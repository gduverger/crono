import requests
import logging

from crono import queue

# DOC
# Bind: http://docs.celeryproject.org/en/latest/userguide/tasks.html#example
# self.request.id, self.request.args, self.request.kwargs
# Name: http://docs.celeryproject.org/en/latest/userguide/tasks.html#names

@queue.queue.task(bind=True, name='crono.tasks.log')
def log(self, level, msg, *args, **kwargs):
	logging.log(level, msg, *args, **kwargs)

@queue.queue.task(bind=True, name='crono.tasks.message')
def message(self, *args, **kwargs):
	raise Exception('`message` task not implemented')

@queue.queue.task(bind=True, name='crono.tasks.request')
def request(self, method, url, **kwargs):
	requests.request(method, url, **kwargs)

@queue.queue.task(bind=True, name='crono.tasks.email')
def email(self, *args, **kwargs):
	raise Exception('`email` task not implemented')
