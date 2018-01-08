# Cryptocurrency-Aribtrage-Trade-Bot

ETH is more expensive at QuadrigaCX than in Kraken.
For example, at this instance, 1 ETH = 0.075500 BTC at Kraken, while 1 ETH = 0.07755823 BTC at QuadrigaCX.
The difference amounts to about 40 CAD.
This trade bot buys ETH with BTC at Kraken, transfers the ETH from Kraken to QuadrigaCX, sells the ETH for BTC at QuadrigaCX, and then transfers the BTC back to Kraken.
Thus, the bot starts with BTC at Kraken, and ETH at QuadrigaCX.
While buying ETH with BTC at Kraken, the bot finds the lowest sellers' ask.
While selling ETH for BTC at QuadrigaCX, the bot find the highest buyers' bid.

## Requirements
- requests
- krakenex
