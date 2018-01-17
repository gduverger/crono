import falcon


class JobsResource(object):

	# def __init__(self, db):
	# 	self.db = db
	# 	self.logger = logging.getLogger(__name__)

	def on_get(self, req, resp):
		"""Handles GET requests"""
		# result = self.db.get_things(marker, limit)

		resp.status = falcon.HTTP_200  # This is the default status
		resp.body = ('Jobs')

	def on_post(self, req, resp):
		# TODO
		pass
