import requests, json
from config import *
import alpaca_trade_api as tradeapi
from yahoo_fin import stock_info as yf
import requests_html
import time

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)


HEADERS = {'APCA-API-KEY-ID': API_KEY, "APCA-API-SECRET-KEY": SECRET_KEY}

quantity = 20

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol":symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)

response = create_order("AAPL", quantity, "buy", "market", "gtc")

print(response)

time.sleep(15)

api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v1')

# Get our position in AAPL.
aapl_position = api.get_position('AAPL')
# Get a list of all of our positions.
portfolio = api.list_positions()
# Print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))


# get live price of Apple
apple_cur_price = yf.get_live_price("aapl")
apple_cur_price = float(apple_cur_price)





def price_of_apple_owned(symbol):

    data = {
        "symbol":symbol
    }
    POS_URL = "{}/v2/positions/AAPL".format(BASE_URL)
    r = requests.get(POS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

response = price_of_apple_owned("AAPL")
#print(response)
print("AVG ENTRY PRICE: "+response['avg_entry_price'])
our_buy_price = int(float(response['avg_entry_price']))

our_buy_price_plus = float(our_buy_price) * float(1.001)



while True:

    def create_order(symbol, qty, side, type, time_in_force):
        data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force
        }
        r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

        return json.loads(r.content)


    time.sleep(120)
    response = create_order("AAPL", quantity, "buy", "market", "gtc")

    print(response)

    time.sleep(15)

    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v1')

    # Get our position in AAPL.
    aapl_position = api.get_position('AAPL')
    # Get a list of all of our positions.
    portfolio = api.list_positions()
    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))

    # get live price of Apple
    apple_cur_price = yf.get_live_price("aapl")


    def price_of_apple_owned(symbol):

        data = {
            "symbol": symbol
        }
        POS_URL = "{}/v2/positions/AAPL".format(BASE_URL)
        r = requests.get(POS_URL, json=data, headers=HEADERS)
        return json.loads(r.content)


    response = price_of_apple_owned("AAPL")
    # print(response)
    print("AVG ENTRY PRICE: " + response['avg_entry_price'])
    our_buy_price = response['avg_entry_price']

    our_buy_price_plus = float(our_buy_price) * float(1.001)

    # get live price of Apple
    apple_cur_price = yf.get_live_price("aapl")
    apple_cur_price = float(apple_cur_price)
    print("CUURENT PRICE BELOW")
    print(apple_cur_price)

    our_buy_price_minus = float(our_buy_price) * float(0.999)
    short_price = ((float(our_buy_price)) - (float(our_buy_price_minus)))

    if apple_cur_price > our_buy_price_plus:
        # then we are going to sell
        # Submit a limit order to attempt to sell 1 share of AAPL at a
        # particular price ($current_price) when the market opens
        api.submit_order(
            symbol='AAPL',
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc',

        )
        print("Selling because price is over 1.001 times our buy price")
        print("Buy Price Below \/")
        print(our_buy_price)

    elif apple_cur_price <= short_price:
        api.submit_order(
            symbol='AAPL',
            qty=quantity,
            side='sell',
            type='limit',
            time_in_force='gtc',
            limit_price=apple_cur_price
        )
        print("Selling because price is 0.999 of our buying price")

    else:
        print("HOLDING")



