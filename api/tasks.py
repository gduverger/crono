import os
import requests
import api.scheduler

from postmarker.core import PostmarkClient


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@api.scheduler.queue.task
def log(message=None):
	# TODO log with timber.io
	print(message)


@api.scheduler.queue.task
def get(url=None):
	requests.get(url)


@api.scheduler.queue.task
def email(to=None, subject=None, body=None):
	postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)
