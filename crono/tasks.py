import requests
import logging

from crono import queue

@queue.queue.task
def log(level, msg, *args, **kwargs):
	logging.log(level, msg, *args, **kwargs)

@queue.queue.task
def message(*args, **kwargs):
	raise Exception('`message` task not implemented')

@queue.queue.task
def request(method, url, **kwargs):
	requests.request(method, url, **kwargs)

@queue.queue.task
def email(*args, **kwargs):
	raise Exception('`email` task not implemented')
