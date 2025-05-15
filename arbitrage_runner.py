import time
from store_data import store_to_supabase
from app import main 

coins = ["ETH", "BTC", "XRP", "ADA", "SOL", "DOGE", "PEPE", "LTC", "DOT", "TRX"]

for coin in coins:
    print(f"\nProcessing {coin}...")

    attempt = 0
    data = None

    while attempt < 3:
        try:
            data = main(coin)
            print(f"[DEBUG] Response for {coin}: {data}")
            all_ops = data.get("all_arbitrage_opportunities", [])

            if all_ops:  
                break
            else:
                print(f"No data returned for {coin}, retrying... ({attempt + 1}/3)")
        except Exception as e:
            print(f"Error processing {coin}: {e}")

        attempt += 1
        time.sleep(2)

    if data and data.get("all_arbitrage_opportunities"):
        store_to_supabase(data)
    else:
        print(f"Failed to get valid data for {coin} after 3 attempts.")

