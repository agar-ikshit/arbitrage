import requests
from .models import ExchangeDataResponse
import logging
logger = logging.getLogger(__name__)





def get_usd_orderbook(coin: str, currency: str = "USDT") -> ExchangeDataResponse | None:

    symbol = f"{coin.upper()}{currency.upper()}"
 
    base_url = "https://api.binance.com/api/v3/depth"
    params = {
        "symbol": symbol,
        "limit": 1
    }
    

    try:
        response = requests.get(base_url, params=params)
        
        response.raise_for_status()
        data = response.json()
        print("Binance raw response:", response.text)

        if "bids" in data and "asks" in data and data["bids"] and data["asks"]:
            best_bid_price = float(data["bids"][0][0])
            best_ask_price = float(data["asks"][0][0])

            return ExchangeDataResponse(
                exchange="Binance",
                symbol=f"{coin.upper()}/{currency.upper()}",
                best_bid_price=best_bid_price,
                best_ask_price=best_ask_price
            )
        else:
            print("Error or empty order book:", data)
            return None
    except requests.RequestException as e:
        print(f"Error fetching Binance data: {e}")
        print(symbol)
        print(coin)
        return None


if __name__ == "__main__":
    print(get_usd_orderbook("BTC"))
