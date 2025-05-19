import requests
from .models import ExchangeDataResponse

def get_usd_orderbook(coin: str, currency: str = "USD") -> ExchangeDataResponse | None:
    pair = f"{coin.upper()}USD"
    url = f"https://api.kraken.com/0/public/Depth?pair={pair}&count=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Kraken returns data keyed by a specific pair name (e.g., XXBTZUSD)
        result_key = list(data['result'].keys())[0]
        orderbook = data['result'][result_key]

        # Each bid/ask is [price, volume, timestamp]
        best_bid_price = float(orderbook['bids'][0][0])
        best_bid_quantity = float(orderbook['bids'][0][1])

        best_ask_price = float(orderbook['asks'][0][0])
        best_ask_quantity = float(orderbook['asks'][0][1])

        return ExchangeDataResponse(
            exchange="Kraken",
            symbol=f"{coin.upper()}/{currency.upper()}",
            best_bid_price=best_bid_price,
            best_bid_quantity=best_bid_quantity,
            best_ask_price=best_ask_price,
            best_ask_quantity=best_ask_quantity
        )

    except Exception as e:
        print(f"Error fetching Kraken data: {e}")
        return None
