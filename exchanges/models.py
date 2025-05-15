import json

class ExchangeDataResponse:
    def __init__(self, exchange: str, symbol: str, best_bid_price: float, best_ask_price: float):
        self.exchange = exchange
        self.symbol = symbol
        self.best_bid_price = best_bid_price
        self.best_ask_price = best_ask_price

    def to_dict(self):
        return {
            "exchange": self.exchange,
            "symbol": self.symbol,
            "best_bid_price": self.best_bid_price,
            "best_ask_price": self.best_ask_price
        }

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)