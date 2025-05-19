import sys, os, time, json
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from exchanges.models import ExchangeDataResponse
from exchanges.kraken import get_usd_orderbook as fetch_kraken
from exchanges.independent_reserve import get_sgd_orderbook as fetch_independent
from exchanges.coinswitch import get_inr_orderbook as fetch_coinswitch
from utils.currency_rates import calculate_rates
from utils.arbitrage import find_best_arbitrage_opportunity

def fetch_all_data(coin: str):
    with ThreadPoolExecutor() as executor:
        future_kraken = executor.submit(fetch_kraken, coin, "USDT")
        future_independent = executor.submit(fetch_independent, coin)  
        future_coinswitch = executor.submit(fetch_coinswitch, coin)    

        kraken_data = future_kraken.result()
        independent_data = future_independent.result()
        coinswitch_data = future_coinswitch.result()

    return [kraken_data, independent_data, coinswitch_data]

def main(coin="XRP"):
    exchange_data = fetch_all_data(coin)
    

    rates = calculate_rates()

    best, all_ops = find_best_arbitrage_opportunity(exchange_data, rates,coin)

    response = {
        "best_arbitrage_opportunity": best,
        "all_arbitrage_opportunities": sorted(all_ops, key=lambda x: x['profit_percentage'], reverse=True)
    }

    return json.dumps(response, indent=4)

if __name__ == "__main__":
    try:
        while True:
            result = main()  
            print(result)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
