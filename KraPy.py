import krakenex

'''
----------
Kraken
----------
'''

class Kra:

    def __init__(self, api_key, private_key):
        self.api_key = api_key
        self.private_key = private_key
        self.bc = 'XXBTZCAD'  # abbreviate the names of the pairs of cryptocurrencies
        self.bu = 'XXBTZUSD'  # i.e. bc stands for Bitcoin to Canadian dollars or vice versa
        self.eb = 'XETHXXBT'  # and 'XXBTZCAD' is the corresponding code that Kraken API recognizes
        self.ec = 'XETHZCAD'
        self.lb = 'XLTCXXBT'
        f = open('kraken.key', 'w')
        f.write(self.api_key + '\n' + self.private_key)
        f.close()
        self.api = krakenex.API()
        self.api.load_key('kraken.key')
        self.b_ad = self.bitcoin_deposit()

    '''
    Input
    ----------
    order_book: str
        Kra.bc, Kra.bu, Kra.eb, Kra.ec

    Output
    ----------
    dictionary:
        a = ask array(<price>, <whole lot volume>, <lot volume>),
        b = bid array(<price>, <whole lot volume>, <lot volume>),
        c = last trade closed array(<price>, <lot volume>),
        v = volume array(<today>, <last 24 hours>),
        p = volume weighted average price array(<today>, <last 24 hours>),
        t = number of trades array(<today>, <last 24 hours>),
        l = low array(<today>, <last 24 hours>),
        h = high array(<today>, <last 24 hours>),
        o = today's opening price
    '''

    def current_trading_information(self, order_book):
        return self.api.query_public('Ticker', {'pair': order_book})['result'][order_book]

    '''
    Input
    ----------
    order_book: Kra.bc, Kra.bu, Kra.eb, Kra.ec

    Output
    ----------
    dictionary
        asks = ask side array of array entries(<price>, <volume>, <timestamp>)
        bids = bid side array of array entries(<price>, <volume>, <timestamp>)
    '''

    def order_book(self, order_book, count):
        return self.api.query_public('Depth', {'pair': order_book, 'count': str(count)})['result'][order_book]

    '''
    Input
    ----------
    None

    Output
    ----------
    array of asset names and balance amount
    '''

    def account_balance(self):
        return self.api.query_private('Balance')['result']

    '''
    Input
    ----------
    order_book: str
        Kra.bc, Kra.bu, Kra.eb, Kra.ec        
    price: float
    volume: float

    Output
    ----------
    dictionary:
        descr = order description info
            order = order description
            close = conditional close order description (if conditional close set)
        txid = array of transaction ids for order (if order was added successfully)
    '''

    def buy_order(self, order_book, price, volume):
        return self.api.query_private('AddOrder', {'pair': order_book, 'type': 'buy', 'price': price, 'ordertype': 'limit','volume': volume})

    '''
    Input
    ----------
    None

    Output
    ----------
    Kraken BTC wallet address: str
    '''

    def bitcoin_deposit(self):
        return self.api.query_private('DepositAddresses', {'asset': 'XXBT', 'method': 'Bitcoin'})['result'][0][
            'address']

    '''
    Input
    ----------
    amount: float
    address: str

    Output
    ----------
    refid = reference id
    '''

    def ether_withdraw(self, amount, address):
        return self.api.query_private('Withdraw', {'asset': 'XXBT', 'amount': amount, 'key': address})



