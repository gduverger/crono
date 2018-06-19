import typing

from apistar import types, validators

interval_params = validators.Object(
	additional_properties=False,
	required=['seconds'],
	properties=[
		('seconds', validators.Integer(minimum=60*5))
	]
)

interval = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['interval'])),
		('params', interval_params),
	]
)

crontab_params = validators.Object(
	additional_properties=False,
	required=['expression'],
	properties=[
		('expression', validators.String())
	]
)

crontab = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['crontab'])),
		('params', crontab_params)
	]
)

get_params = validators.Object(
	required=['url'],
	additional_properties=False,
	properties=[
		('url', validators.String(pattern=r'^http.*'))
	]
)

get = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['get', 'BUG'])),
		('params', get_params)
	]
)

email_params = validators.Object(
	required=['to', 'subject', 'body'],
	additional_properties=False,
	properties=[
		('to', validators.String(pattern=r'[^@]*@[^@]*.[^@]*')),
		('subject', validators.String(max_length=100)),
		('body', validators.String(max_length=100))
	]
)

email = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['email'])),
		('params', email_params)
	]
)

log_params = validators.Object(
	required=['message'],
	additional_properties=False,
	properties=[
		('message', validators.String())
	]
)

log = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['log'])),
		('params', log_params)
	]
)

class Job(types.Type):

	trigger = interval | crontab
	task = get | email # | log

	def __init__(self, *args, **kwargs):
		value = super().__init__(*args, **kwargs)
		# Additional validation
		return value
