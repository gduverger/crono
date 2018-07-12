import time

from apistar import App, exceptions, http
from api import models


class TimingHook:

	def on_request(self):
		self.started = time.time()

	def on_response(self):
		duration = time.time() - self.started
		print('Response returned in {:0.6f} seconds.'.format(duration))


class AuthenticationHook:

	def on_request(self, app: App, request: http.Request, user: models.User=None) -> None:

		# HACK
		public_routes = [
			app.reverse_url('get_index'),
			# app.reverse_url('post_user'),
		]

		if user is None and request.url.components.path not in public_routes:
			raise exceptions.Forbidden('Not authenticated')


class ErrorHook:

	def on_response(self, response: http.Response, exc: Exception):
		if exc is None:
			print('Handler returned a response')
		else:
			print('Exception handler returned a response')
			

	def on_error(self, response: http.Response): # -> http.Response:
		print('An unhandled error was raised')
		# response.content = 'Internal Server Error'
		# response.status_code = 500
		# response.headers = 
