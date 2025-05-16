from fastapi import FastAPI, Query
from concurrent.futures import ThreadPoolExecutor


from exchanges.models import ExchangeDataResponse
from exchanges.kraken import get_usd_orderbook as fetch_kraken
from exchanges.independent_reserve import get_sgd_orderbook as fetch_independent
from exchanges.coinswitch import get_inr_orderbook as fetch_coinswitch
from utils.currency_rates import calculate_rates
from utils.arbitrage import find_best_arbitrage_opportunity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Or ["*"] to allow all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main(coin: str):

                   

    with ThreadPoolExecutor() as executor:
        future_kraken = executor.submit(fetch_kraken, coin)
        future_independent = executor.submit(fetch_independent, coin)
        future_coinswitch = executor.submit(fetch_coinswitch, coin)

        kraken_data = future_kraken.result()
        independent_data = future_independent.result()
        coinswitch_data = future_coinswitch.result()

    rates = calculate_rates()

    exchange_data = [kraken_data, independent_data, coinswitch_data]
    best, all_ops = find_best_arbitrage_opportunity(exchange_data, rates,coin)

    response = {
        "best_arbitrage_opportunity": best,
        "all_arbitrage_opportunities": sorted(all_ops, key=lambda x: x['profit_percentage'], reverse=True)
    }

    return response

@app.get("/arbitrage")
def get_arbitrage_data(coin: str = Query("XRP", description="Coin symbol, e.g. XRP, BTC, ETH")):
    return main(coin)
