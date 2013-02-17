class Book(object):
	def __init__(self, isbn, title, rrp, current_price):
		self.isbn = isbn
		self.title = title
		self.rrp = rrp
		self.current_price = current_price

	def __str__(self):
		return u'{0}, {1}, {2}, {3}'.format(self.title, self.isbn, self.rrp, self.current_price)