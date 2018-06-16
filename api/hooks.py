import time

from apistar import exceptions, http
from api import components


class TimingHook:

	def on_request(self):
		self.started = time.time()

	def on_response(self):
		duration = time.time() - self.started
		print('Response returned in {:0.6f} seconds.'.format(duration))


class AuthenticationHook:

	def on_request(self, user: components.User=None) -> None:
		if user is None:
			raise exceptions.Forbidden('Not authenticated')


class ErrorHook:

	def on_response(self, response: http.Response, exc: Exception):
		if exc is None:
			print('Handler returned a response')
		else:
			print('Exception handler returned a response')

	def on_error(self, response: http.Response):
		print('An unhandled error was raised')
