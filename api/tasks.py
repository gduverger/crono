import os
import logging
import timber
import requests
import api.scheduler

from postmarker.core import PostmarkClient
from api import models


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))
timber = timber.TimberHandler(api_key=os.getenv('TIMBER_API_KEY'))
# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(timber)


@api.scheduler.queue.task
def log(job_key, message=None):

	try:
		models.Job.get_by_key(job_key).add_log()
		logger.info('log')

	except Exception as error:
		logger.critical(error, extra={'job_key': job_key, 'url': url})


@api.scheduler.queue.task
def get(job_key, url=None):

	try:
		models.Job.get_by_key(job_key).add_log()
		requests.get(url, timeout=60) # 1 minute

	except Exception as error:
		logger.critical(error, extra={'job_key': job_key, 'url': url})


@api.scheduler.queue.task
def email(job_key, to=None, subject=None, body=None):
	
	try:
		models.Job.get_by_key(job_key).add_log()
		postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)

	except Exception as error:
		logger.critical(error, extra={'job_key': job_key, 'to': to, 'subject': subject, 'body': body})
