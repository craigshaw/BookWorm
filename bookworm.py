#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	BookWorm application.
"""

from atexit import register
from apscheduler.scheduler import Scheduler
import logging
import pickle
import os
import argparse

from model.stores.amazon import AmazonStore
from notification.notifymyandroid import NotifyMyAndroid

args = None

class Application(object):
	def __init__(self):
		self.books = []
		self.logger = logging.getLogger(__name__)
		self.scheduler = Scheduler()

		self.scheduler.add_interval_job(self.process_book_list, seconds=30)

		self.store = AmazonStore()
		self.notifier = NotifyMyAndroid(args.key)

		self.load()

	def load(self):
		if os.path.exists('books.dat'):
			with open('books.dat', 'rb') as f:
				self.books = pickle.load(f)
				self.logger.debug('Loaded {0} books'.format(len(self.books)))

	def save(self):
		if(len(self.books) > 0 ):
			with open('books.dat', 'wb') as f:
				self.logger.debug('Saving books')
				pickle.dump(self.books, f, -1)

	def start(self):
		self.logger.info('Starting application')
		self.scheduler.start()

	def stop(self):
		self.logger.info('Stopping application')
		self.save()
		self.scheduler.shutdown()

	def process_book_list(self):
		self.logger.info('Processing book list')

		for book in self.books:
			self.logger.debug('Updating price for {0}'.format(book.title))
			latestPrice = self.store.get_book_price(book.isbn)
			self.logger.debug('latest: {0}, saved: {1}'.format(latestPrice, book.current_price))

			if latestPrice != None and latestPrice != book.current_price:
				if latestPrice < book.current_price:
					self.logger.debug('Found a lower price!')
					self.notifier.send_notification(self.build_notification_message(latestPrice, book.isbn, book.title), 'Price Update')

				book.current_price = latestPrice

	def build_notification_message(self, price, isbn, title):
		return (u'{0} is now £{1}\nhttp://www.amazon.co.uk/gp/product/{2}'.format(title, price, isbn))

	def get_resolver(self):
		return self.store.get_book_details

	def register_new_book(self, book):
		self.books.append(book)

def main():
	logging.basicConfig(filename='log.txt', level=logging.DEBUG)
	# Tweak log level for scheduler
	logging.getLogger('apscheduler').setLevel(logging.ERROR)

	application = Application()
	application.start()

	@register
	def on_exit():
		application.stop()
	
	process_cli(application)

def process_cli(application):
	command = ' '

	while command != 'q' and command != 'Q':
		command = raw_input('>> ')

		if command == 'i' or command == 'I':
			insert_new_book(application)
		elif command == 'd' or command == 'D':
			for book in application.books:
				print(book)
		elif command == 'f' or command == 'F':
			for book in application.books:
				book.current_price = 99.99

def insert_new_book(application):
	isbn = raw_input('ISBN: ')

	resolver = application.get_resolver()

	if resolver != None:
		book = resolver(isbn)

		if book != None:
			print('Resolved book: {0}'.format(book))
			application.register_new_book(book)

def crack_args():
	parser = argparse.ArgumentParser(description='Bookworm book monitor and notifier')
	parser.add_argument('-k', dest='key', help='Notifymyandroid key')
	parser.add_argument('-p', dest='port', default=15009, type=int, help='Administrative port')
	parser.add_argument('-d', dest='daemonise', action='store_true', help='Run as daemon')

	return parser.parse_args()

if __name__ == '__main__':
	try:
		args = crack_args()
		print(args)
		main()
	except (KeyboardInterrupt, SystemExit):
		pass