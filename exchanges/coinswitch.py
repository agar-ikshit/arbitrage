import socketio
import time
from .models import ExchangeDataResponse 

base_url = "wss://ws.coinswitch.co/"
namespace = "/coinswitchx"
socketio_path = "/pro/realtime-rates-socket/spot/coinswitchx"
EVENT_NAME = "FETCH_ORDER_BOOK_CS_PRO"

def get_inr_orderbook(coin: str) -> ExchangeDataResponse | None:
    pair = f"{coin.upper()},INR"
    sio = socketio.Client()

    exchange_data = {}

    @sio.on(EVENT_NAME, namespace=namespace)
    def on_order_book(data):
        nonlocal exchange_data
        if 'bids' in data and 'asks' in data:
            best_bid = data['bids'][0] if data['bids'] else None
            best_ask = data['asks'][0] if data['asks'] else None

            if best_bid and best_ask:
                best_bid_price = float(best_bid[0])
                best_bid_quantity = float(best_bid[1])
                best_ask_price = float(best_ask[0])
                best_ask_quantity = float(best_ask[1])

                exchange_data = ExchangeDataResponse(
                    exchange="CoinSwitch",
                    symbol=pair,
                    best_bid_price=best_bid_price,
                    best_bid_quantity=best_bid_quantity,
                    best_ask_price=best_ask_price,
                    best_ask_quantity=best_ask_quantity
                )
                sio.disconnect()

    try:
        sio.connect(
            url=base_url,
            namespaces=[namespace],
            transports=['websocket'],
            socketio_path=socketio_path,
            wait=True,
            wait_timeout=10
        )

        sio.emit(EVENT_NAME, {'event': 'subscribe', 'pair': pair}, namespace=namespace)
        time.sleep(5)

    except Exception as e:
        print(f"[CoinSwitch] WebSocket error: {e}")
        return None

    return exchange_data if exchange_data else None

if __name__ == "__main__":
    result = get_inr_orderbook("BTC")
    print(result.to_json() if result else "No data")
