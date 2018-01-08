import requests
import time
import hmac
import hashlib

'''
----------
QuadrigaCX
----------
'''

class Qua:

    def __init__(self, client_id, api_key, api_secret):
        self.client_id = client_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.bc = 'btc_cad'     # Here, we abbreviate the names of the cryptocurrencies orderbooks,
        self.bu = 'btc_usd'     # i.e. bc stands for the exchange between bitcoins and Canadian dollars,
        self.eb = 'eth_btc'     # and 'btc_cad' is the corresponding code that QuadrigaCX API recognizes
        self.ec = 'eth_cad'
        self.lc = 'ltc_cad'
        self.lb = 'ltc_btc'
        self.e_ad = self.ether_deposit()    # e_ad stands for ethereum address

    def payload(self):
        nonce = str(int(time.time() * 1000))
        message = bytes(nonce + self.client_id + self.api_key, 'utf-8')
        secret = bytes(self.api_secret, 'utf-8')
        signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
        payload = {}
        payload['key'] = self.api_key
        payload['nonce'] = nonce
        payload['signature'] = signature
        return payload

    '''
    Input
    ----------
    order_book: str
        Qua.bc, Qua.bu, Qua.eb, or Qua.ec

    Output
    ----------
    dictionary:
        last - last BTC price
        high - last 24 hours price high
        low - last 24 hours price low
        vwap - last 24 hours volume weighted average price: vwap
        volume - last 24 hours volume
        bid - highest buy order
        ask - lowest sell order
    '''

    def current_trading_information(self, order_book):
        return requests.get('https://api.quadrigacx.com/v2/ticker?book=' + order_book).json()

    '''
    Input
    ----------
    order_book: str
        Qua.bc, Qua.bu, Qua.eb, or Qua.ec

    Output
    ----------
    dictionary with "bids" and "asks". Each is a list of open orders and each order is represented as a list of price and amount.
    '''

    def order_book(self, order_book):
        payload = {'book': order_book}
        return requests.get('https://api.quadrigacx.com/v2/order_book', params=payload).json()

    '''
    Input
    ----------
    order_book: str
        Qua.bc, Qua.bu, Qua.eb, or Qua.ec
    time: str
        'minute' or 'hour'

    Output
    ----------
    dictionary:
        date - unix timestamp date and time
        tid - transaction id
        price - BTC price
        amount - BTC amount
        side - The trade side indicates the maker order side (maker order is the order that was open on the order book)
    '''

    def transactions(self, order_book, time):
        my_payload = {'book': order_book, 'time': time}
        return requests.get('https://api.quadrigacx.com/v2/transactions', params=my_payload).json()

    '''
    Input
    ----------
    None

    Output
    ----------
    dictionary:
        cad_balance - CAD balance
        btc_balance - BTC balance
        cad_reserved - CAD reserved in open orders
        btc_reserved - BTC reserved in open orders
        cad_available - CAD available for trading
        btc_available - BTC available for trading
        fee - customer trading fee
    '''

    def account_balance(self):
        return requests.post('https://api.quadrigacx.com/v2/balance', json=self.payload()).json()

    '''
    Input
    ----------
    offset - skip that many transactions before beginning to return results. Default: 0.
    limit - limit result to that many transactions. Default: 100.
    sort - sorting by date and time (asc - ascending; desc - descending). Default: desc.
    order_book: str
        self.bc, self.bu, self.eb, or self.ec

    Output
    ----------
    dictionary:
        datetime - date and time
        id - unique identifier (only for trades)
        type - transaction type (0 - deposit; 1 - withdrawal; 2 - trade)
        method - deposit or withdrawal method
        (minor currency code) - the minor currency amount
        (major currency code) - the major currency amount
        order_id - a 64 character long hexadecimal string representing the order that was fully or partially filled (only for trades)
        fee - transaction fee
        rate - rate per btc (only for trades)
    '''

    def user_transactions(self, offset, limit, sort, order_book):
        my_payload = self.payload()
        my_payload['offset'] = offset
        my_payload['limit'] = limit
        my_payload['sort'] = sort
        my_payload['book'] = order_book
        return requests.post('https://api.quadrigacx.com/v2/user_transactions', json=my_payload).json()

    '''
    Input
    ----------
    order_book: str
        Qua.bc, Qua.bu, Qua.eb, or Qua.ec

    Output
    ----------
    dictionary:
        id - order id
        datetime - date and time
        type - buy or sell (0 - buy; 1 - sell)
        price - price
        amount - amount
        status - status of the order (0 - active; 1 - partially filled)
    '''

    def open_orders(self, book):
        my_payload = self.payload()
        my_payload['book'] = book
        return requests.post(url='https://api.quadrigacx.com/v2/open_orders', json=my_payload).json()

    '''
    Input
    ----------
    id - a single or array of 64 characters long hexadecimal string taken from the list of orders

    Output
    ----------
    dictionary:
        id - the order id passed to that function
        order_book: str
        price - price of the order
        amount - amount of the order
        type - buy or sell (0 - buy; 1 - sell)
        status - status of the order (-1 - canceled; 0 - active; 1 - partially filled; 2 - complete)
        created - date the order was created
        updated - date the order was last updated (not shown when status = 0)
    '''

    def lookup_order(self, id):
        my_payload = self.payload()
        my_payload['id'] = id
        return requests.post('https://api.quadrigacx.com/v2/lookup_order', json=my_payload).json()

    '''
    Input
    ----------
    dictionary:
    id - a 64 characters long hexadecimal string taken from the list of orders

    Output
    ----------
    'true' if order has been found and canceled.
    '''

    def cancel_order(self, id):
        my_payload = self.payload()
        my_payload['id'] = id
        return requests.post('https://api.quadrigacx.com/v2/cancel_order', json=my_payload).json()

    '''
    Input
    ----------
    order_book: str
        Qua.bc, Qua.bu, Qua.eb, or Qua.ec
    amount - amount of major currency
    price - price to buy at

    Output
    ----------
    dictionary:
        id - order id
        datetime - date and time
        type - buy or sell (0 - buy; 1 - sell)
        price - price
        amount - amount
    '''

    def buy_order(self, order_book, price, amount):
        my_payload = self.payload()
        my_payload['book'] = order_book
        my_payload['price'] = price
        my_payload['amount'] = amount
        return requests.post(url='https://api.quadrigacx.com/v2/buy', json=my_payload).json()

    '''
    Input
    ----------
    order_book: str
        self.bc, self.bu, self.eb, or self.ec
    amount - amount of major currency
    price - price to sell at

    Output
    ----------
    dictionary:
        id - order id
        datetime - date and time
        type - buy or sell (0 - buy; 1 - sell)
        price - price
        amount - amount
    '''

    def sell_order(self, order_book, price, amount):
        my_payload = self.payload()
        my_payload['amount'] = amount
        my_payload['price'] = price
        my_payload['book'] = order_book
        return requests.post('https://api.quadrigacx.com/v2/sell', json=my_payload).json()

    '''
    Input
    ----------
    None

    Output
    ----------
    Bitcoin deposit address for funding your account.
    '''

    def bitcoin_deposit(self):
        my_payload = self.payload()
        return requests.post('https://api.quadrigacx.com/v2/bitcoin_deposit_address', json=my_payload).json()

    '''
    Input
    ----------
    amount - The amount to withdraw
    address: str
        The bitcoin address we will send the amount to

    Output
    ----------
    OK or error
    '''

    def bitcoin_withdraw(self, amount, address):
        my_payload = self.payload()
        my_payload['amount'] = amount
        my_payload['address'] = address
        return requests.post('https://api.quadrigacx.com/v2/bitcoin_withdrawal', json=my_payload).json()

    '''
    Input
    ----------
    None

    Output
    ----------
    Ethereum deposit address for funding your account.
    '''

    def ether_deposit(self):
        my_payload = self.payload()
        return requests.post('https://api.quadrigacx.com/v2/ether_deposit_address', json=my_payload).json()

    '''
    Input
    ----------
    amount - The amount to withdraw
    address - The ethereum address we will send the amount to

    Output
    ----------
    OK or error
    '''

    def ether_withdraw(self, amount, address):
        my_payload = self.payload()
        my_payload['amount'] = amount
        my_payload['address'] = address
        return requests.post('https://api.quadrigacx.com/v2/ether_withdrawal', json=my_payload).json()
