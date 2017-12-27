# Cryptos

I am looking to build simple tools to allow users to interact with Cryptos in a fun, easy and meaningful way.

Currently the project has:

1. A script to find the price of a certain crypto. This uses coinmarketcap.com as the source for the data. To use: 
 - Download `altcoin-price.py`
 - Edit the name of the coin you are looking for in the code. 
 - Run `python altcoin-price.py` in your terminal

 This is not a particularly useful script right now. However, it will be adjusted to include the coin name in the command line to be more usable. More importantly, this functionality was used and automated for the slack bot project.

2. A slackbot built on top of the price script to build "Price Bot" so users can interact with the bot and find prices in slack. Price Bot comes equipped with 3 primary commands: `price`, `coinbase` and `bitstamp` (as well as `help` and `say`). Price Bot is constantly gaining functionality. Future goals include: 
 - Extract information from more exchanges
 - Instant notifications if a coin is doing particularly well or badly

3. Open to other ideas!
