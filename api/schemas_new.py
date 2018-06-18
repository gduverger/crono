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

trigger_crontab = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['crontab'])),
		('params', validators.Ref('CrontabParams'))
	],
	definitions={
		'CrontabParams': validators.Object(
			additional_properties=False,
			required=['expression'],
			properties=[
				('expression', validators.String())
			]
		)
	}
)

class Job(types.Type):

	trigger = interval | trigger_crontab

	def __init__(self, *args, **kwargs):
		value = super().__init__(*args, **kwargs)
		# Additional validation
		return value
