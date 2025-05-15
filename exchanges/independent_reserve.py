import requests
from .models import ExchangeDataResponse  



def get_sgd_orderbook(coin: str, currency: str = "SGD") -> ExchangeDataResponse | None:
    url = "https://api.independentreserve.com/Public/GetMarketSummary"
    params = {
        "primaryCurrencyCode": coin.upper(),
        "secondaryCurrencyCode": currency.upper()
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        best_bid = float(data["CurrentHighestBidPrice"])
        best_ask = float(data["CurrentLowestOfferPrice"])

        return ExchangeDataResponse(
            exchange="Independent Reserve",
            symbol=f"{coin.upper()}/{currency.upper()}",
            best_bid_price=best_bid,
            best_ask_price=best_ask
        )

    except requests.RequestException as e:
        print(f"Error fetching Independent Reserve data: {e}")
        return None

# if __name__ == "__main__":
#     print(get_sgd_orderbook("XRP"))
