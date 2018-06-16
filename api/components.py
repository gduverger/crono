import os
import base64

from apistar import exceptions, http
from apistar.server.components import Component


class User(object):

	def __init__(self, token: str):
		self.token = token


class UserComponent(Component):

	def resolve(self, authorization: http.Header) -> User:
		"""
		Determine the user associated with a request, using HTTP Basic Authentication.
		"""
		if authorization is None:
			return None

		scheme, token = authorization.split()
		if scheme.lower() != 'bearer':
			return None

		token = base64.b64decode(token).decode('utf-8')
		if not self.check_authentication(token):
			raise exceptions.Forbidden('Incorrect token')

		return User(token)

	def check_authentication(self, token: str) -> bool:
		# Just an example here. You'd normally want to make a database lookup,
		# and check against a hash of the password.
		return token == os.getenv('USER_TOKEN')
