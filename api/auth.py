# DOC: https://github.com/requests/requests/issues/4437

import requests

class HTTPBearerAuth(requests.auth.AuthBase):
	def __init__(self, token):
		self.token = token

	def __eq__(self, other):
		return self.token == getattr(other, 'token', None)

	def __ne__(self, other):
		return not self == other

	def __call__(self, r):
		r.headers['Authorization'] = 'Bearer ' + self.token
		return r
