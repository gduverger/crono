import os
import logging
import timber
import requests
import api.scheduler

from postmarker.core import PostmarkClient


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))
timber = timber.TimberHandler(api_key=os.getenv('TIMBER_API_KEY'))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(timber)


@api.scheduler.queue.task
def log(message=None):
	logger.info('Log: {}'.format(message), extra={'meta': 'test'})


@api.scheduler.queue.task
def get(url=None):
	requests.get(url)


@api.scheduler.queue.task
def email(to=None, subject=None, body=None):
	postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)
