#######################################
# Script to get the price of alt-coins
# at a particular time. 
# Can be adapted for a slack bot.
# 
# Author: @rsichel107
#######################################

# import libraries
import urllib2
from bs4 import BeautifulSoup

coin = 'bitcoin' # Put your coin name here
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
	print coin + " is currently $" + price 