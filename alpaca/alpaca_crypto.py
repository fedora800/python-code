#import alpaca_trade_api as tradeapi
import requests, json


# crypto paper trading connection info
PAPER_TRADING_APCA_API_BASE_URL  = "https://paper-api.alpaca.markets"
PAPER_TRADING_APCA_API_KEY_ID  = "PK37G13YXFINIKE7Z98O"
PAPER_TRADING_APCA_API_SECRET_KEY = "bWet0HFG7s5asf7LMiFubPabJjAlSoloNsocOPRg"
PAPER_TRADING_HEADERS = {'APCA-API-KEY-ID': PAPER_TRADING_APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': PAPER_TRADING_APCA_API_SECRET_KEY}
PAPER_TRADING_ACCOUNT_URL = "{}/v2/account".format(PAPER_TRADING_APCA_API_BASE_URL)
PAPER_TRADING_ORDERS_URL = "{}/v2/orders".format(PAPER_TRADING_APCA_API_BASE_URL)
PAPER_TRADING_POSITIONS_URL = "{}/v2/positions".format(PAPER_TRADING_APCA_API_BASE_URL)


# def get_account():
#     r = requests.get(ACCOUNT_URL, headers=HEADERS)
#     return json.loads(r.content)


def get_account_using_alpaca_trade_api():
    api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL)
    
    # Get account info
    account = api.get_account()

    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')

def get_account_details():
    r = requests.get(PAPER_TRADING_ACCOUNT_URL, headers=PAPER_TRADING_HEADERS)
    print(r.content)
    return json.loads(r.content)


def get_orders():                   # are these open or filled ones too ?
    r = requests.get(PAPER_TRADING_ORDERS_URL, headers=PAPER_TRADING_HEADERS)
    print(r.content)
    return json.loads(r.content)


def create_and_send_order(symbol, quantity, side, type, time_in_force):
    order_data = {
        "symbol" : symbol,
        "qty" : quantity,
        "side" : side,
        "type" : type,
        "time_in_force" : time_in_force
    }

    r = requests.post(PAPER_TRADING_ORDERS_URL, json=order_data, headers=PAPER_TRADING_HEADERS)
    return json.loads(r.content)


def get_open_positions():
    r = requests.get(PAPER_TRADING_POSITIONS_URL, headers=PAPER_TRADING_HEADERS)
    print(r.content)
    return json.loads(r.content)




if __name__ == '__main__':
    print("--here 1--")
    get_account_details()
    #r = requests.get("https://paper-api.alpaca.markets/v2/account", headers={'APCA-API-KEY-ID': PAPER_TRADING_APCA_API_KEY_ID, 'APCA-API-SECRET-KEY': PAPER_TRADING_APCA_API_SECRET_KEY})
    #r = requests.get(PAPER_TRADING_ACCOUNT_URL, headers=PAPER_TRADING_HEADERS)
    #print(r.content)
    print("--here 2--")

    #order_send_response = create_and_send_order("AAPL", 100, "buy", "market", "day")
    #order_send_response = create_and_send_order("BTCUSD", 0.01, "buy", "market", "day")
    #print(order_send_response)
    print("--here 3--")
    
    orders_response = get_orders()
    print(orders_response)
    print("--here 4--")

    open_positions_response = get_open_positions()
    print(open_positions_response)
    print("--here 5--")


