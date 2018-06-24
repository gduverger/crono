import os
import base64

from api import database
from apistar import exceptions, http
from apistar.server.components import Component


class AuthorizationComponent(Component):

	def resolve(self, authorization: http.Header) -> database.User:
		"""
		Determine the user associated with a request, using HTTP Basic Authentication.
		"""
		if authorization is None:
			return None

		scheme, token = authorization.split()
		if scheme.lower() != 'bearer':
			return None

		user = database.User.get_user(token)

		if not user:
			raise exceptions.Forbidden('Incorrect token')

		return user
