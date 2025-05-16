import requests
from .models import ExchangeDataResponse

def get_usd_orderbook(coin: str, currency: str = "USD") -> ExchangeDataResponse | None:
    product_id = f"{coin.upper()}-{currency.upper()}"
    url = f"https://api.pro.coinbase.com/products/{product_id}/book"
    params = {"level": 1}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        best_bid = float(data["bids"][0][0])
        best_ask = float(data["asks"][0][0])

        return ExchangeDataResponse(
            exchange="Coinbase Pro",
            symbol=f"{coin.upper()}/{currency.upper()}",
            best_bid_price=best_bid,
            best_ask_price=best_ask
        )
    except requests.RequestException as e:
        print(f"Error fetching Coinbase data: {e}")
        return None
