FEE_CONFIG = {
    "Kraken": {
        "taker_fee_percent": 0.26,
        "withdrawal_fee": {
            "BTC": 0.00015,
            "ETH": 0.0035,
            "XRP": 0.02,
            "ADA": 1.0,
            "SOL": 0.01,
            "DOGE": 5.0,
            "PEPE": 1000000,   # a
            "DOT": 0.1,
            "TRX": 1.0
        }
    },
    "Independent Reserve": {
        "taker_fee_percent": 0.5,
        "withdrawal_fee": {
            "BTC": 0.0002,
            "ETH": 0.005,
            "XRP": 0.15,
            "ADA": 0.5,
            "SOL": 0.001,
            "DOGE": 5.0,
            "PEPE": 500000,    # a
            "LTC": 0.0015,     # a
            "DOT": 0.1,
            "TRX": 1.0         # a
        }
    },
    "CoinSwitch": {
        "taker_fee_percent": 1.0,  # a conservative 
        "withdrawal_fee": {
            "BTC": 0.00025,    # a
            "ETH": 0.005,      
            "XRP": 0.02,       
            "ADA": 0.8,        
            "SOL": 0.002,      
            "DOGE": 3.0,      
            "PEPE": 1000000,  
            "LTC": 0.002,      
            "DOT": 0.08,       
            "TRX": 1.0         
        }
    }
}
