import os
import requests
import logging

from crono import queue


@queue.queue.task
def log(level, msg, *args, **kwargs):
	logging.log(level, msg, *args, **kwargs)


@queue.queue.task
def message(*args, **kwargs):
	# TODO Twilio integration
	raise Exception('message task not implemented')


@queue.queue.task
def request(method, url, **kwargs):
	requests.request(method, url, **kwargs)


@queue.queue.task
def email(*args, **kwargs):
	# TODO Postmark integration
	raise Exception('email task not implemented')


@queue.queue.task
def printf(text, *args, **kwargs):
	data = {'text': text, 'args': args, 'kwargs': kwargs}
	return requests.post('https://printf-prod.herokuapp.com/' + os.getenv('PRINTF_ROOM', 'crono'), data=data)
