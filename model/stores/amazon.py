from urllib import urlencode
import urllib2
from bs4 import BeautifulSoup
from model.book import Book

class AmazonStore(object):
	def __init__(self):
		pass

	def get_product_url(self, isbn):
		return 'http://www.amazon.co.uk/gp/product/{0}'.format(isbn)

	def get_book_price(self, isbn):
		price = None
		f = urllib2.urlopen(self.get_product_url(isbn))
		parser = BeautifulSoup(f.read())
		priceTag = parser.find(self.price_finder)

		if priceTag != None:
			price = float(priceTag.string[1:].encode('utf-8', 'xmlcharrefreplace'))

		return price

	def supports_resolution(self):
		return true

	def get_book_details(self, isbn):
		f = urllib2.urlopen(self.get_product_url(isbn))
		parser = BeautifulSoup(f.read())

		price = rrp = title = 'Not found'

		# Get the current price
		priceTag = parser.find(self.price_finder)
		if priceTag != None:
			price = float(priceTag.string[1:].encode('utf-8', 'xmlcharrefreplace'))

		# Get the RRP
		rrpTag = parser.find(self.rrp_finder)
		if rrpTag != None:
			rrp = float(rrpTag.string[1:].encode('utf-8', 'xmlcharrefreplace'))

		# Get the title
		titleTag = parser.find(self.title_finder)
		if titleTag != None:
	 		title = ' '.join(titleTag.stripped_strings)

		return Book(isbn,title,rrp,price)

	def price_finder(self, tag):
		return tag.name == 'b' and tag.has_key('class') and tag['class'][0] == u'priceLarge' and not tag.has_key('style')

	def title_finder(self, tag):
		return tag.name == 'span' and tag.has_key('id') and tag['id'] == u'btAsinTitle'

	def rrp_finder(self, tag):
		return tag.name == 'span' and tag.has_key('id') and tag['id'] == u'listPriceValue' and tag.has_key('class') and tag['class'][0] == u'listprice'
