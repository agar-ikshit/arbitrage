import sys, os, time, json
from concurrent.futures import ThreadPoolExecutor

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from exchanges.models import ExchangeDataResponse
from exchanges.binance import get_usd_orderbook as fetch_binance
from exchanges.independent_reserve import get_sgd_orderbook as fetch_independent
from exchanges.coinswitch import get_inr_orderbook as fetch_coinswitch
from utils.currency_rates import calculate_rates
from utils.arbitrage import find_best_arbitrage_opportunity

def fetch_all_data(coin: str):
    with ThreadPoolExecutor() as executor:
        # Launch calls concurrently, respecting currency for each exchange
        future_binance = executor.submit(fetch_binance, coin, "USDT")
        future_independent = executor.submit(fetch_independent, coin)  # assumes function updated to accept coin param
        future_coinswitch = executor.submit(fetch_coinswitch, coin)    # also updated to accept coin param

        # Gather results
        binance_data = future_binance.result()
        independent_data = future_independent.result()
        coinswitch_data = future_coinswitch.result()

    return [binance_data, independent_data, coinswitch_data]

def main(coin="XRP"):
    # 1) Fetch all data concurrently
    exchange_data = fetch_all_data(coin)

    # 2) Fetch exchange rates
    rates = calculate_rates()

    # 3) Compute arbitrage
    best, all_ops = find_best_arbitrage_opportunity(exchange_data, rates,coin)

    # 4) Build JSON response
    response = {
        "best_arbitrage_opportunity": best,
        "all_arbitrage_opportunities": sorted(all_ops, key=lambda x: x['profit_percentage'], reverse=True)
    }

    return json.dumps(response, indent=4)

if __name__ == "__main__":
    try:
        while True:
            result = main()  # You can pass different coins here if you want
            print(result)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")
