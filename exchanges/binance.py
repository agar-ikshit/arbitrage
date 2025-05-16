import requests
from .models import ExchangeDataResponse
import logging

logger = logging.getLogger(__name__)

def get_usd_orderbook(coin: str, currency: str = "USDT") -> ExchangeDataResponse | None:
    symbol = f"{coin.upper()}{currency.upper()}"
    url = f"https://api.binance.com/api/v3/ticker/bookTicker"

    params = {
        "symbol": symbol
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "bidPrice" in data and "askPrice" in data:
            best_bid_price = float(data["bidPrice"])
            best_ask_price = float(data["askPrice"])

            return ExchangeDataResponse(
                exchange="Binance",
                symbol=f"{coin.upper()}/{currency.upper()}",
                best_bid_price=best_bid_price,
                best_ask_price=best_ask_price
            )
        else:
            print("Unexpected response format:", data)
            return None
    except requests.RequestException as e:
        print(f"Error fetching Binance data: {e}")
        print(symbol)
        print(coin)
        return None

if __name__ == "__main__":
    print(get_usd_orderbook("BTC"))
