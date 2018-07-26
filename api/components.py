import os
import base64

from api import models
from apistar import exceptions, http
from apistar.server.components import Component


class AuthorizationComponent(Component):

	def resolve(self, authorization: http.Header) -> models.User:
		"""
		Determine the user associated with a request, using HTTP Basic Authentication.
		"""

		if authorization is None:
			return None

		scheme, token = authorization.split()
		if scheme.lower() != 'bearer':
			return None

		user = models.User.get(token)

		if not user or not user.is_active:
			raise exceptions.Forbidden('Incorrect token. Email {} for help.'.format(os.getenv('CRONO_SUPPORT_EMAIL')))

		return user
