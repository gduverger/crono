import datetime

from api import main, scheduler


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
	func = 'api:commands.email'

	@staticmethod
	def callable(to, subject, body):
		# TODO queue?
		main.postmark.emails.send(From='log@airquote.co', To=to, Subject=subject, TextBody=body)

def email(to, subject, body):
	main.postmark.emails.send(From='log@airquote.co', To=to, Subject=subject, TextBody=body)


class LogCommand(Command):
	
	NAME = 'log'
	KEYS = ('message',)
	func = 'api:commands.log'

	@staticmethod
	def callable(message):
		# TODO queue?
		print(message)

def log(message):
	print(message)


class CommandException(Exception):
	pass


@scheduler.queue.task
def add(x, y):
	return x + y
