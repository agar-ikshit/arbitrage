import requests
from .models import ExchangeDataResponse  

def get_sgd_orderbook(coin: str, currency: str = "SGD") -> ExchangeDataResponse | None:
    url = "https://api.independentreserve.com/Public/GetOrderBook"
    params = {
        "primaryCurrencyCode": coin.upper(),
        "secondaryCurrencyCode": currency.upper()
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract best bid and ask from BuyOrders and SellOrders
        best_bid_order = data['BuyOrders'][0] if data['BuyOrders'] else None
        best_ask_order = data['SellOrders'][0] if data['SellOrders'] else None

        if not best_bid_order or not best_ask_order:
            print("Order book is empty")
            return None

        best_bid_price = float(best_bid_order['Price'])
        best_bid_quantity = float(best_bid_order['Volume'])
        best_ask_price = float(best_ask_order['Price'])
        best_ask_quantity = float(best_ask_order['Volume'])

        return ExchangeDataResponse(
            exchange="Independent Reserve",
            symbol=f"{coin.upper()}/{currency.upper()}",
            best_bid_price=best_bid_price,
            best_bid_quantity=best_bid_quantity,
            best_ask_price=best_ask_price,
            best_ask_quantity=best_ask_quantity
        )

    except requests.RequestException as e:
        print(f"Error fetching Independent Reserve data: {e}")
        return None
