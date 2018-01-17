import os
import json
import falcon

from crono import app
from apscheduler.jobstores.base import JobLookupError


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Doc(object):

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.content_type = falcon.MEDIA_JSON
		with open('{}/doc.json'.format(DIR_PATH), 'r') as file:
			resp.body = file.read()


class Jobs(object):

	# def __init__(self, db):
	#   self.db = db
	#   self.logger = logging.getLogger(__name__)

	def on_get(self, req, resp):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)
		jobs = app.scheduler.get_jobs()

		resp.status = falcon.HTTP_200
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'job_ids': [job.id for job in jobs]})

	def on_post(self, req, resp):
		job = app.scheduler.add_job(task, 'interval', minutes=1)

		resp.status = falcon.HTTP_201
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'job_id': job.id})


class Job(object):

	def on_get(self, req, resp, job_id):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)
		job = app.scheduler.get_job(job_id)

		resp.status = falcon.HTTP_200  # This is the default status
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'job_id': job.id if job else None})

	def on_delete(self, req, resp, job_id):
		# resp.content_type = falcon.MEDIA_JSON

		try:
			app.scheduler.remove_job(job_id)
			resp.status = falcon.HTTP_200

		except JobLookupError as e:
			resp.status = falcon.HTTP_204


def task():
	print('task')
