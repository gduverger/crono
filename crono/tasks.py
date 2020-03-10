import os
import requests
# import postmarker

from crono import queue


@queue.queue.task
def log(string):
	if string:
		print(string)

	raise Exception('log task not valid')


@queue.queue.task
def message(**kwargs):
	# TODO Twilio integration
	raise Exception('message task not implemented')


@queue.queue.task
def request(method, url, **kwargs):
	requests.request(method, url, **kwargs)


@queue.queue.task
def email(**kwargs):
	# TODO Postmark integration
	raise Exception('email task not implemented')
