from urllib import urlencode
import urllib2
import logging

notificationKey = "3709f6800c75e40c3a02a5c493015868c97af8e9534d6564"
notificationRoot = "https://www.notifymyandroid.com/publicapi/notify"

class NotifyMyAndroid(object):
	def __init__(self,key=notificationKey):
		self.key = key
		self.logger = logging.getLogger(__name__)

	def send_notification(self, message, event):
		data = urlencode([('apikey',self.key),('application','BookWorm'),('event',event),('description',unicode(message).encode('utf-8'))])

		self.logger.debug('Payload: {0}'.format(data))

		request = urllib2.Request(url=notificationRoot, data=data)
		f = urllib2.urlopen(request)
		response = f.read()

		self.logger.debug('Response: {0}'.format(response))