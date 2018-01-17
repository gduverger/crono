import json
import falcon


class Tests(object):

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'test': True})


class Jobs(object):

	# def __init__(self, db):
	# 	self.db = db
	# 	self.logger = logging.getLogger(__name__)


	def on_get(self, req, resp):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)

		resp.status = falcon.HTTP_200  # This is the default status
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps({'test': True})


	def on_post(self, req, resp):
		# TODO
		resp.status = falcon.HTTP_201
