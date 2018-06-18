from apistar import types, validators

trigger_interval_params = validators.Object(
	additional_properties=False,
	required=['seconds'],
	properties=[
		('seconds', validators.Integer(minimum=300)) # 5 minutes
	]
)

trigger_interval = validators.Object(
	required=['name', 'params'],
	additional_properties=False,
	properties=[
		('name', validators.String(enum=['interval'])),
		('params', trigger_interval_params)
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

	trigger = trigger_interval | trigger_crontab

	def __init__(self, *args, **kwargs):
		value = super().__init__(*args, **kwargs)
		# Additional validation
		return value
