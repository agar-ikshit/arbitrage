def find_best_arbitrage_opportunity(exchanges, exchange_rates, coin):
    """Returns:
    - best_opportunity: dict
    - all_opportunities: list of dict
    """
    best_profit = float('-inf')
    best_opportunity = None
    all_opportunities = []

    # Define quote currencies
    exchange_quote_currency = {
        "Binance": "USD",
        "Independent Reserve": "SGD",
        "CoinSwitch": "INR"
    }

    for buy in exchanges:
        if not buy:
            continue

        for sell in exchanges:
            if not sell or buy.exchange == sell.exchange:
                continue

            # Get currencies
            buy_currency = exchange_quote_currency.get(buy.exchange, "INR")
            sell_currency = exchange_quote_currency.get(sell.exchange, "INR")

            # Convert buy price to INR
            buy_price = buy.best_ask_price
            if buy_currency == "USD":
                buy_price_in_inr = buy_price * exchange_rates.get("USD/INR", 1)
            elif buy_currency == "SGD":
                buy_price_in_inr = buy_price * exchange_rates.get("SGD/INR", 1)
            else:
                buy_price_in_inr = buy_price

            # Convert sell price to INR
            sell_price = sell.best_bid_price
            if sell_currency == "USD":
                sell_price_in_inr = sell_price * exchange_rates.get("USD/INR", 1)
            elif sell_currency == "SGD":
                sell_price_in_inr = sell_price * exchange_rates.get("SGD/INR", 1)
            else:
                sell_price_in_inr = sell_price

            # Sanity check: prevent division by tiny amounts
            if buy_price_in_inr < 1e-6:
                continue

            profit = sell_price_in_inr - buy_price_in_inr
            profit_percentage = (profit / buy_price_in_inr) * 100

            opportunity = {
                "coin": coin,
                "buy_from": buy.exchange,
                "sell_to": sell.exchange,
                "buy_price_original": round(buy_price, 7),
                "buy_price_in_inr": round(buy_price_in_inr, 7),
                "buy_original_currency": buy_currency,
                "sell_price_original": round(sell_price, 7),
                "sell_price_in_inr": round(sell_price_in_inr, 7),
                "sell_original_currency": sell_currency,
                "profit_in_inr": round(profit, 4),
                "profit_percentage": round(profit_percentage, 4),
            }

            all_opportunities.append(opportunity)

            if profit_percentage > best_profit:
                best_profit = profit_percentage
                best_opportunity = opportunity

    return best_opportunity, all_opportunities
