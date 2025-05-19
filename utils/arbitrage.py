from .fee_config import FEE_CONFIG


def find_best_arbitrage_opportunity(exchanges, exchange_rates, coin):
    best_profit = float('-inf')
    best_opportunity = None
    all_opportunities = []

    exchange_quote_currency = {
        "Kraken": "USD",
        "Independent Reserve": "SGD",
        "CoinSwitch": "INR"
    }

    for buy in exchanges:
        if not buy:
            continue

        for sell in exchanges:
            if not sell or buy.exchange == sell.exchange:
                continue

            buy_currency = exchange_quote_currency.get(buy.exchange, "INR")
            sell_currency = exchange_quote_currency.get(sell.exchange, "INR")

            buy_price = buy.best_ask_price
            sell_price = sell.best_bid_price

            if buy_currency == "USD":
                buy_price_in_inr = buy_price * exchange_rates.get("USD/INR", 1)
            elif buy_currency == "SGD":
                buy_price_in_inr = buy_price * exchange_rates.get("SGD/INR", 1)
            else:
                buy_price_in_inr = buy_price

            if sell_currency == "USD":
                sell_price_in_inr = sell_price * exchange_rates.get("USD/INR", 1)
            elif sell_currency == "SGD":
                sell_price_in_inr = sell_price * exchange_rates.get("SGD/INR", 1)
            else:
                sell_price_in_inr = sell_price

            if buy_price_in_inr < 1e-6 or sell_price_in_inr < 1e-6:
                continue

            # Calculate gross profit and percentage
            gross_profit = sell_price_in_inr - buy_price_in_inr
            gross_profit_percentage = (gross_profit / buy_price_in_inr) * 100

            if gross_profit <= 0 or gross_profit_percentage <= 0:
                continue

            if gross_profit < 0.00001 or gross_profit_percentage < 0.1:
                continue

            # Calculate fees
            buy_fee_percent = FEE_CONFIG.get(buy.exchange, {}).get("taker_fee_percent", 0) / 100
            sell_fee_percent = FEE_CONFIG.get(sell.exchange, {}).get("taker_fee_percent", 0) / 100

            buy_withdraw_fee_coin = FEE_CONFIG.get(buy.exchange, {}).get("withdrawal_fee", {}).get(coin, 0) or 0
            sell_withdraw_fee_coin = FEE_CONFIG.get(sell.exchange, {}).get("withdrawal_fee", {}).get(coin, 0) or 0

            # Convert withdrawal fees to INR (using buy currency for buy withdrawal, sell currency for sell withdrawal)
            def convert_withdraw_fee_to_inr(exchange, currency, fee_coin):
                if fee_coin == 0:
                    return 0
                if currency == "USD":
                    return fee_coin * exchange_rates.get("USD/INR", 1)
                elif currency == "SGD":
                    return fee_coin * exchange_rates.get("SGD/INR", 1)
                elif currency == "INR":
                    return fee_coin
                else:
                    return fee_coin  # fallback

            buy_withdraw_fee_inr = convert_withdraw_fee_to_inr(buy.exchange, buy_currency, buy_withdraw_fee_coin)
            sell_withdraw_fee_inr = convert_withdraw_fee_to_inr(sell.exchange, sell_currency, sell_withdraw_fee_coin)

            # Estimate net buy cost: buy price + taker fee + withdrawal fee
            # Taker fee on buy is on the purchase amount
            net_buy_price_inr = buy_price_in_inr * (1 + buy_fee_percent) + buy_withdraw_fee_inr

            # Estimate net sell revenue: sell price - taker fee - withdrawal fee
            net_sell_price_inr = sell_price_in_inr * (1 - sell_fee_percent) - sell_withdraw_fee_inr

            net_profit = net_sell_price_inr - net_buy_price_inr
            net_profit_percentage = (net_profit / net_buy_price_inr) * 100 if net_buy_price_inr else -float('inf')

            if net_profit <= 0 or net_profit_percentage <= 0:
                continue

            opportunity = {
                "coin": coin,
                "buy_from": buy.exchange,
                "sell_to": sell.exchange,
                "buy_price_original": round(buy_price, 8),
                "buy_price_in_inr": round(buy_price_in_inr, 8),
                "buy_original_currency": buy_currency,
                "buy_quantity": round(getattr(buy, "best_ask_quantity", 0), 8),
                "sell_price_original": round(sell_price, 8),
                "sell_price_in_inr": round(sell_price_in_inr, 8),
                "sell_original_currency": sell_currency,
                "sell_quantity": round(getattr(sell, "best_bid_quantity", 0), 8),
                "profit_in_inr": round(gross_profit, 6),
                "profit_percentage_before_fees": round(gross_profit_percentage, 4),
                "profit_percentage_after_fees": round(net_profit_percentage, 4),
            }

            all_opportunities.append(opportunity)

            if net_profit_percentage > best_profit:
                best_profit = net_profit_percentage
                best_opportunity = opportunity

    return best_opportunity, all_opportunities
