import os
import requests
# import postmarker

from crono import queue


# postmark = postmarker.core.PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@queue.queue.task
def log(string):
	print(string)


@queue.queue.task
def message(**kwargs):
	# TODO Twilio integration
	raise Exception('Not implemented')


@queue.queue.task
def request(method, url, **kwargs):
	requests.request(method, url, **kwargs)


@queue.queue.task
def email(**kwargs):
	#postmark.emails.send(**kwargs)
	raise Exception('Not implemented')
