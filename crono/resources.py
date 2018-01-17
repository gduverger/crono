import json
import falcon


class Test(object):

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'test': True})


class Jobs(object):

	# def __init__(self, db):
	#   self.db = db
	#   self.logger = logging.getLogger(__name__)

	def on_get(self, req, resp):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)
		# TODO get_job()
		resp.status = falcon.HTTP_200  # This is the default status
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'jobs': [1,2,3]})

	def on_post(self, req, resp):
		# TODO get_job()
		resp.status = falcon.HTTP_201


class Job(object):

	def on_get(self, req, resp, job_id):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)
		# TODO get_job()
		resp.status = falcon.HTTP_200  # This is the default status
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'job': job_id})

	def on_delete(self, req, resp, job_id):
		# TODO remove_job()
		resp.status = falcon.HTTP_201
		resp.content_type = falcon.MEDIA_JSON
