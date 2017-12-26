import os
import time
import re
import gdax
from slackclient import SlackClient
import urllib2
from bs4 import BeautifulSoup

## Slackbot to get the price of certain cryptos from www.coinmarketcap.com
## With help from: https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
## GDAX Puthon API: https://github.com/danpaquin/gdax-python

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "help"
MENTION_REGEX = "^<@(|[WU].+)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Type 'price' followed by the name of the crypto and I will give you the price of that currency. For example: price ripple \n"
        response += "Or, type 'coinbase' and I will give you the current prices on Coinbase"
    if command.startswith("price"):
    	try:
    		response = get_price(command.split(" ")[1])
    	except: 
    		response = "What currency do you want to see? I know a bunch!"
    if command.startswith("coinbase"):
    	slack_client.api_call(
        	"chat.postMessage",
        	channel=channel,
        	text="Checking coinbase prices, hold on!"
    	)
    	response = coinbase()

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

## Get the price for a given coin from coinmarketcap.com
def get_price(coin):
	isCoin = False
	response = None 
	default_response = "Not sure what you mean. These are the coins I know: bitcoin, ethereum, litecoin, bitcoin-cash, bitcoin-gold, ripple, iota, zcash, dash and monero. If you want more, talk to Rebecca. I'm just a bot!"
	# Determine if this is a valid coin
	coinlist = ['bitcoin', 'ethereum', 'bitcoin-cash', 'bitcoin-gold','ripple', 'litecoin', 'iota', 'zcash', 'dash', 'monero']
	tickerlist = ['btc', 'eth', 'bch', 'btg', 'xrp', 'ltc', 'miota', 'zec', 'dash', 'xmr']
	html_info = ['id-bitcoin', 'id-ethereum', 'id-bitcoin-cash', 'id-bitcoin-gold', 'id-ripple', 'id-litecoin', 'id-iota', 'id-zcash', 'id-dash', 'id-monero']
	if coin.lower() in coinlist: 
		isCoin = True
	if coin.lower() in tickerlist:
		isCoin = True
	if isCoin:
		try:
			ind = coinlist.index(coin.lower())
		except: 
			ind = tickerlist.index(coin.lower())
		htmltag = html_info[ind] 
		# specify the url
		price_page = 'https://coinmarketcap.com/coins/'

		# query the website and return the html to the variable 
		contents = urllib2.urlopen(price_page)

		# parse the html using beautiful soup and store in variable
		page = BeautifulSoup(contents, 'html.parser')

		# Take out the proper row
		row = page.find('tr', attrs={'id': htmltag})

		price_box = row.find('td', attrs= {'class': 'no-wrap text-right'})

		price = (price_box.a).get('data-usd')
		response = coin + " is currently $" + price 
	
	return response or default_response

## Get the current prices from Coinbase
def coinbase():
	btc = "Bitcoin is: $"
	bch = "Bitcoin Cash is: $"
	eth = "Ether is: $"
	ltc = "Litecoin is: $"

	public_client = gdax.PublicClient()
	BTC = public_client.get_product_ticker(product_id='BTC-USD')
	for key in BTC:
		if str(key) == "price":
			btc += str(BTC[key]) + "\n"
	BCH = public_client.get_product_ticker(product_id='BCH-USD')
	for key in BCH:
		if str(key) == "price":
			bch += str(BCH[key]) + "\n"
	ETH = public_client.get_product_ticker(product_id='ETH-USD')
	for key in ETH:
		if str(key) == "price":
			eth += str(ETH[key]) + "\n"
	LTC = public_client.get_product_ticker(product_id='LTC-USD')
	for key in LTC:
		if str(key) == "price":
			ltc += str(LTC[key]) + "\n"
	return btc + bch + eth + ltc


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Price Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")