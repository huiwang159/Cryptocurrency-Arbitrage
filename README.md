# Cryptocurrency-Aribtrage-Trade-Bot

## Introduction
Ethereum (ETH) is more expensive at QuadrigaCX than at Kraken. For example, at an instance during programming this bot, 1 ETH = 0.075500 Bitcoin (BTC) at Kraken, while 1 ETH = 0.07755823 BTC at QuadrigaCX. The difference amounts to about 40 CAD. This offers an arbitrage oppurtunity.

## Summary
This bot buys ETH with BTC at Kraken, transfers the ETH from Kraken to QuadrigaCX, sells the ETH for BTC at QuadrigaCX, and then transfers the BTC back to Kraken.

## Requirements
- [requests](http://docs.python-requests.org/en/master/)
- [krakenex](https://github.com/veox/python3-krakenex)

## Usage
In the terminal, run
```
python3 bot qua_client_id qua_api_key qua_api_secret kra_api_key kra_private_key minutes
```
where 
- qua_client_id is the QuadrigaCX client ID
- qua_api_key is the QuadrigaCX API key
- kra_api_key is the Kraken API key
- kra_private_key is the Kraken Private Key
- minutes is the number of minutes to run the bot
