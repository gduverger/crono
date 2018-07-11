import os
import logging
# import timber
import requests
import api.scheduler

from postmarker.core import PostmarkClient
from api import models


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))
# timber = timber.TimberHandler(api_key=os.getenv('TIMBER_API_KEY'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.addHandler(timber)


@api.scheduler.queue.task
def log(job_key, message=None):
	extra = {'job_key': job_key, 'message_': message}

	try:
		models.Job.get_by_key(job_key).add_log()
		logger.info('Task: log', extra=extra)

	except Exception as error:
		logger.error(error, extra=extra, exc_info=True)


@api.scheduler.queue.task
def get(job_key, url=None):
	extra = {'job_key': job_key, 'url': url}

	try:
		models.Job.get_by_key(job_key).add_log()
		requests.get(url, timeout=60) # 1 minute
		logger.info('Task: get', extra=extra)

	except Exception as error:
		logger.error(error, extra=extra, exc_info=True)


@api.scheduler.queue.task
def email(job_key, to=None, subject=None, body=None):
	extra = {'job_key': job_key, 'to': to, 'subject': subject, 'body': body}

	try:
		models.Job.get_by_key(job_key).add_log()
		postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)
		logger.info('Task: email', extra=extra)

	except Exception as error:
		logger.error(error, extra=extra, exc_info=True)
