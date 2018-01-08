# Cryptocurrency-Aribtrage-Trade-Bot

## Introduction
Ethereum (ETH) is more expensive at QuadrigaCX than at Kraken. For example, at an instance during programming this bot, 1 ETH = 0.075500 Bitcoin (BTC) at Kraken, while 1 ETH = 0.07755823 BTC at QuadrigaCX. The difference amounts to about 40 CAD. This offers an arbitrage oppurtunity.

## Summary
This bot buys ETH with BTC at Kraken, transfers the ETH from Kraken to QuadrigaCX, sells the ETH for BTC at QuadrigaCX, and then transfers the BTC back to Kraken.

## Requirements
- requests("http://docs.python-requests.org/en/master/")
- krakenex("https://github.com/veox/python3-krakenex")

## Usage
