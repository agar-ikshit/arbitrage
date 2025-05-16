from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def store_to_supabase(data):
    best = data.get("best_arbitrage_opportunity")
    all_ops = data.get("all_arbitrage_opportunities", [])

    # Generate a single timestamp for this run
    run_timestamp = datetime.utcnow().isoformat()

    # Store best opportunity if it's profitable
    if best and best["profit_percentage"] > 0:
        insert_opportunity(best, is_best=True, timestamp=run_timestamp)

    # Store other profitable opportunities
    for op in all_ops:
        if op["profit_percentage"] > 0 and op != best:
            insert_opportunity(op, is_best=False, timestamp=run_timestamp)

def insert_opportunity(opportunity, is_best=False, timestamp=None):
    data = {
        "coin": opportunity["coin"],
        "buy_from": opportunity["buy_from"],
        "sell_to": opportunity["sell_to"],
        "buy_price_original": opportunity["buy_price_original"],
        "buy_price_in_inr": opportunity["buy_price_in_inr"],
        "buy_original_currency": opportunity["buy_original_currency"],
        "sell_price_original": opportunity["sell_price_original"],
        "sell_price_in_inr": opportunity["sell_price_in_inr"],
        "sell_original_currency": opportunity["sell_original_currency"],
        "profit_in_inr": opportunity["profit_in_inr"],
        "profit_percentage": opportunity["profit_percentage"],
        "is_best": is_best,
        "timestamp": timestamp  # manually setting same timestamp
    }

    response = supabase.table("arbitrage_opportunities").insert(data).execute()

    if response.data:
        print(f"Inserted opportunity for {opportunity['coin']}")
    else:
        print(f"Insert failed for {opportunity['coin']}: {response.error}")
