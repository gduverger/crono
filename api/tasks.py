import os
import requests

from postmarker.core import PostmarkClient
from api import models, scheduler
from apistar import exceptions


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@scheduler.queue.task
def log(job_key, message=None):

	try:
		job = models.Job.get_by_key(job_key)
		job.add_log()
		job.incr_exec()

	except Exception as error:
		pass


@scheduler.queue.task
def request(job_key, method='GET', url=None):

	try:
		
		if method in ['GET', 'get']:
			requests.get(url, timeout=60) # 1 minute

		elif method in ['POST', 'post']:
			requests.post(url, timeout=60) # 1 minute

		else:
			# TODO surface this exception
			exceptions.MethodNotAllowed("Method '{}' not implemented yet".format(method))

		models.Job.get_by_key(job_key).incr_exec()

	except Exception as error:
		# TODO
		pass


@scheduler.queue.task
def email(job_key, to=None, subject=None, body=None):

	try:
		postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)
		models.Job.get_by_key(job_key).incr_exec()

	except Exception as error:
		# TODO
		pass
