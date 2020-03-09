import os
import requests

from postmarker.core import PostmarkClient
from api import models, queue


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@queue.queue.task
def log(message=None):

	try:
		job = models.Job.get_by_key(job_key)
		job.add_log()
		job.incr_exec()

	except Exception as error:
		pass


@queue.queue.task
def message():
	pass


@queue.queue.task
def request(method='GET', url=None):

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


@queue.queue.task
def email(to=None, subject=None, body=None):

	try:
		postmark.emails.send(From=os.getenv('FROM_EMAIL_ADDRESS'), To=to, Subject=subject, TextBody=body)
		models.Job.get_by_key(job_key).incr_exec()

	except Exception as error:
		# TODO
		pass
