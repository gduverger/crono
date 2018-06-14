import os
import requests
import api.scheduler

from postmarker.core import PostmarkClient


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@api.scheduler.queue.task
def log(message=None):
	print(message)


@api.scheduler.queue.task
def get(url=None):
	requests.get(url)


@api.scheduler.queue.task
def email(to=None, subject=None, body=None):
	postmark.emails.send(From='crono@gduverger.com', To=to, Subject=subject, TextBody=body)
