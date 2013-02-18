from urllib import urlencode
import urllib2
import logging

notificationRoot = "https://www.notifymyandroid.com/publicapi/notify"

class NotifyMyAndroid(object):
	def __init__(self,key):
		self.key = key
		self.logger = logging.getLogger(__name__)

	def send_notification(self, message, event):
		data = urlencode([('apikey',self.key),('application','BookWorm'),('event',event),('description',unicode(message).encode('utf-8'))])

		self.logger.debug('Payload: {0}'.format(data))

		request = urllib2.Request(url=notificationRoot, data=data)
		f = urllib2.urlopen(request)
		response = f.read()

		self.logger.debug('Response: {0}'.format(response))