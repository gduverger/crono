from apistar import types, validators

interval_params = validators.Object(
	additional_properties=False,
	required=['seconds'],
	properties=[
		('seconds', validators.Integer(minimum=300, default=3600)) # 5 minutes, 1 hour
	]
)

class Job(types.Type):

	trigger = validators.Object(
		properties=[
			('trigger', )
		]
		# Interval
		validators.Object(
			# required=['name', 'params'],
			additional_properties=False,
			properties=[
				('name', validators.String(enum=['interval', 'foo'])),
				('params', validators.Ref('IntervalParams'))
			],
			definitions={
				'IntervalParams': validators.Object(
					additional_properties=False,
					required=['seconds'],
					properties=[
						('seconds', validators.Integer(minimum=300, default=3600)) # 5 minutes, 1 hour
					]
				)
			}
		),

		# Crontab
		validators.Object(
			# required=['name', 'params'],
			additional_properties=False,
			properties=[
				('name', validators.String(enum=['crontab', 'bar'])),
				('params', validators.Ref('CrontabParams'))
			],
			definitions={
				'CrontabParams': validators.Object(
					additional_properties=False,
					required=['expression'],
					properties=[
						('expression', validators.String())
					],
				)
			}
		),

		# ETA
		# validators.Object(
		# 	required=['name', 'params'],
		# 	additional_properties=False,
		# 	properties=[
		# 		('name', validators.String(enum=['eta'])),
		# 		('params', validators.Ref('EtaParams'))
		# 	],
		# 	definitions={
		# 		'EtaParams': validators.Object(
		# 			additional_properties=False,
		# 			required=['datetime'],
		# 			properties=[
		# 				('datetime', validators.String(format='datetime'))
		# 			]
		# 		)
		# 	}
		# ),

		# Countdown
		# validators.Object(
		# 	required=['name', 'params'],
		# 	additional_properties=False,
		# 	properties=[
		# 		('name', validators.String(enum=['countdown'])),
		# 		('params', validators.Ref('CountdownParams'))
		# 	],
		# 	definitions={
		# 		'CountdownParams': validators.Object(
		# 			additional_properties=False,
		# 			required=['seconds'],
		# 			properties=[
		# 				('seconds', validators.String(format='datetime'))
		# 			]
		# 		)
		# 	}
		# ),

	)

	task = validators.Union(items=[

		# Log
		validators.Object(definitions={
			'name': validators.String(enum=['log', 'foo']),
			'params': validators.Object(definitions={
				'message': validators.String(max_length=100)
			}) # , required=['message']
		}, required=['name', 'params']), # additional_properties=False

		# Email
		validators.Object(definitions={
			'name': validators.String(enum=['email', 'foo']),
			'params': validators.Object(definitions={
				'to': validators.String(pattern=r'[^@]*@[^@]*.[^@]*'),
				'subject': validators.String(max_length=100),
				'body': validators.String(max_length=100)
			}) # , required=['to', 'subject', 'body']
		}, required=['name', 'params']), # additional_properties=False

		# GET
		validators.Object(definitions={
			'name': validators.String(enum=['get', 'foo']),
			'params': validators.Object(definitions={
				'url': validators.String(pattern='^http.*')
			}) # , required=['url']
		}, required=['name', 'params']) # additional_properties=False
	])

	def __init__(self, *args, **kwargs):
		value = super().__init__(*args, **kwargs)
		# Additional validation
		return value
