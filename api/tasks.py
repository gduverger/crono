import os
import logging
import requests
import api.scheduler

from postmarker.core import PostmarkClient
from api import models
from apistar import exceptions


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))
logger = logging.getLogger(__name__)


@api.scheduler.queue.task
def log(job_key, message=None):

	try:
		models.Job.get_by_key(job_key).add_log()
		logger.info(__name__, extra=locals())

	except Exception as error:
		logger.error(error, extra=locals(), exc_info=True)


@api.scheduler.queue.task
def request(job_key, method='GET', url=None):

	try:
		models.Job.get_by_key(job_key).add_log()
		logger.info(__name__, extra=locals())
		
		if method in ['GET', 'get']:
			requests.get(url, timeout=60) # 1 minute

		elif method in ['POST', 'post']:
			requests.post(url, timeout=60) # 1 minute

		else:
			# TODO surface this exception
			exceptions.MethodNotAllowed("Method '{}' not implemented yet".format(method))

	except Exception as error:
		logger.error(error, extra=locals(), exc_info=True)


@api.scheduler.queue.task
def email(job_key, to=None, subject=None, body=None):

	try:
		models.Job.get_by_key(job_key).add_log()
		logger.info(__name__, extra=locals())

		postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)

	except Exception as error:
		logger.error(error, extra=locals(), exc_info=True)
