import time
import json
from store_data import store_to_supabase
from app import main

coins = ["ETH", "BTC", "XRP", "ADA", "SOL", "DOGE", "PEPE", "LTC", "DOT", "TRX"]

for coin in coins:
    print(f"\nProcessing {coin}...")

    attempt = 0
    data = None

    while attempt < 3:
        try:
            result = main(coin)  
            print(f"[DEBUG] Raw response for {coin}: {result}")

            if isinstance(result, str):
                data = json.loads(result)  # parse only if string
            elif isinstance(result, dict):
                data = result
            else:
                raise TypeError(f"Unexpected return type: {type(result)}")

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
        try:
            store_to_supabase(data)
            print(f"Stored arbitrage data for {coin}")
        except Exception as e:
            print(f"Failed to store data for {coin}: {e}")
    else:
        print(f"Failed to get valid data for {coin} after 3 attempts.")
