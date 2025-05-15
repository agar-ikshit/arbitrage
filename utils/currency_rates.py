import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get your API key for ExchangeRate API
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

def get_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()

    if data["result"] != "success":
        raise Exception("Error fetching exchange rates.")
    

    
    return data["conversion_rates"].get(target_currency)

def calculate_rates():
    # Fetch USD to INR, USD to SGD, and USDT to INR
    sgd_inr = get_exchange_rate("SGD", "INR")
    usdt_inr = get_exchange_rate("USD", "INR")
    
    return {
        "SGD/INR": sgd_inr,
        "USD/INR": usdt_inr
    }


# try:
#     rates = calculate_rates()
#     print(f"Exchange Rates:\nSGD/INR: {rates['SGD/INR']}\nUSD/INR: {rates['USD/INR']}")
# except Exception as e:
#     print(f"Error: {e}")
