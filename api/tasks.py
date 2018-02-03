import datetime

from api import main, scheduler


class Task(object):

	def __init__(self, params):
		self.params = {}

		for key in self.KEYS:
			if params.get(key):
				self.params[key] = params[key]

		if len(self.KEYS) > len(self.params):
			raise TaskException('Missing task parameters')

	@staticmethod
	def init(params):
		name = None

		# Name
		if params.get('name'):
			name = params['name']
		else:
			raise TaskException('Missing task name')

		# Class
		if name == EmailTask.NAME:
			return EmailTask(params)
		if name == LogTask.NAME:
			return LogTask(params)
		else:
			raise TaskException('Invalid task name')

	@property
	def name(self):
		return self.NAME


class EmailTask(Task):
	
	NAME = 'email'
	KEYS = ('to', 'subject', 'body')
	func = 'api:tasks.email'

	@staticmethod
	def callable(to, subject, body):
		# TODO queue?
		main.postmark.emails.send(From='log@airquote.co', To=to, Subject=subject, TextBody=body)

def email(to, subject, body):
	main.postmark.emails.send(From='log@airquote.co', To=to, Subject=subject, TextBody=body)


class LogTask(Task):
	
	NAME = 'log'
	KEYS = ('message',)
	func = 'api:tasks.log'

	@staticmethod
	def callable(message):
		# TODO queue?
		print(message)

def log(message):
	print(message)


class TaskException(Exception):
	pass


@scheduler.queue.task
def add(x, y):
	return x + y
