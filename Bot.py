#!/bin/python3
from QuaPy import *
from KraPy import *
import time
import logging
import sys

class Bot:
    def __init__(self, qua_client_id, qua_api_key, qua_api_secret, kra_api_key, kra_private_key):
        print('Creating log')
        logging.basicConfig(filename='Log', level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s')
        logger = logging.getLogger('\t__init__')
        try:
            # Set up Kraken and QuadrigaCX APIs
            print('Setting up Kraken API')
            self.kra = Kra(kra_api_key, kra_private_key)
            print('Setting up QuadrigaCX API')
            self.qua = Qua(qua_client_id, qua_api_key, qua_api_secret)
            # Calculate fees
            self.fees = (1-0.26/100)*(1-0.2/100)    # Kraken BTC to ETH exchange fees is 0.26%.
                                                    # QuadrigaCX ETH to BTC exchange fees is 0.20%.
                                                    # ETH withdrawal from Kraken costs 0.005 ETH,
                                                    # which is factored in later in the calculate method.
                                                    # BTC withdrawal from QuadrigaCX is free.
            logger.info('\tAPI setup successful')
            print('API setup successful')
        except Exception as e:
            logger.error('\t' + str(e))
            print('API setup unsuccessfull. Please check network connection.')

    def start(self, minutes):
        logger = logging.getLogger('\tstart   ')
        sum = 0.0
        last = 0.0
        start = time.time()
        print('Identifying oppurtunities')
        while time.time() < start+ 60 * int(minutes):
            calculations = bot.calculate()
            if calculations is not None:
                profit = calculations[4]
                if profit != last and profit > 0:
                    sum += profit
                    last = profit
                    logger.info('\tEstimated profit: ' + str(profit) + '\tCumulative estimated profit: ' + str(sum))
                    print ('Estimated profit: ' + str(profit) + '\tCumulative estimated profit: ' + str(sum))
                    try:
                        print('Executing arbitrage')
                        self.execute(calculations[0], calculations[1], calculations[2])
                    except Exception as e:
                        if e['error'][0] is 'EOrder:Insufficient funds':
                            self.rebalance()
                        else:
                            logger.error('\t' + str(e))
        return sum

    def calculate(self):
        logger = logging.getLogger('\tcalculate')
        try:
            kra_btc_eth = self.kra.order_book(bot.kra.eb, 1)['asks'][0][:2]
            qua_eth_btc = self.qua.order_book(bot.qua.eb)['bids'][0]
            buy_at  = float(kra_btc_eth[0])
            sell_at = float(qua_eth_btc[0])
            volume = min(float(kra_btc_eth[1]), float(qua_eth_btc[1]))
            gross = sell_at * volume * self.fees - 0.005    # Kraken withdrawal costs 0.005 ETH
            profit = gross - buy_at * volume
            message = 'Buy at: ' + str(buy_at) + '\tSell at: '+ str(sell_at) + '\tVolume: ' + str(volume) + '\tGross: ' + str(gross) + '\tProfit: ' + str(profit)
            logger.info('\t' + message)
            print(message)
            return buy_at, sell_at, volume, gross, profit
        except Exception as e:
            logger.error('\t' + str(e))

    def execute(self, kra_eth_btc, qua_btc_eth, volume):
        logger = logging.getLogger('\texecute')
        try:
            logger.info('\t' + self.kra.buy_order(self.kra.eb, kra_eth_btc, volume))
            logger.info('\t' + self.qua.sell_order(self.qua.eb, qua_btc_eth, volume))
        except Exception as e:
            logger.error('\t' + str(e))

    def rebalance(self):
        logger = logging.getLogger('\trebalance')
        print('Rebalancing Accounts')
        try:
            kra_eth = bot.kra.account_balance()['XETH']             # Get Kraken ETH balance
            qua_btc = bot.qua.account_balance()['btc_available']    # Get QuadrigaCX BTC balance
            bot.qua.bitcoin_withdraw(qua_btc, bot.kra.b_ad)         # Withdraw all Kraken ETH to QuadrigaCX wallet
            bot.kra.ether_withdraw(kra_eth, bot.qua.e_ad)           # Withdraw all QuadrigaCX BTC to Kraken BTC wallet
        except Exception as e:
            logger.error('\t' + str(e))

if __name__ == '__main__':
    bot = Bot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    bot.start(sys.argv[6])