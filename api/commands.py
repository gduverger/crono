import datetime

from api import main, worker


class Command(object):

	def __init__(self, params):
		self.params = {}

		for key in self.KEYS:
			if params.get(key):
				self.params[key] = params[key]

		if len(self.KEYS) > len(self.params):
			raise CommandException('Missing command parameters')

	@staticmethod
	def init(params):
		name = None

		# Name
		if params.get('name'):
			name = params['name']
		else:
			raise CommandException('Missing command name')

		# Class
		if name == EmailCommand.NAME:
			return EmailCommand(params)
		if name == LogCommand.NAME:
			return LogCommand(params)
		else:
			raise CommandException('Invalid command name')

	@property
	def name(self):
		return self.NAME


class EmailCommand(Command):
	
	NAME = 'email'
	KEYS = ('to', 'subject', 'body')

	@staticmethod
	def callable(to, subject, body):
		# TODO queue?
		main.postmark.emails.send(From='log@airquote.co', To=to, Subject=subject, TextBody=body)


class LogCommand(Command):
	
	NAME = 'log'
	KEYS = ('message',)

	@staticmethod
	def callable(message):
		# TODO queue?
		print(message)


class CommandException(Exception):
	pass
