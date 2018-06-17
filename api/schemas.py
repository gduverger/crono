from apistar import types, validators

class Job(types.Type):

	trigger = validators.Union(items=[

		# Interval
		validators.Object(definitions={
			'name': validators.String(enum=['interval']),
			'params': validators.Object(definitions={
				'seconds': validators.Integer(minimum=300, default=3600) # 5 minutes, 1 hour
			})
		}),

		# Crontab
		validators.Object(definitions={
			'name': validators.String(enum=['crontab']),
			'params': validators.Object(definitions={
				'expression': validators.String(pattern='[^\s]* [^\s]* [^\s]* [^\s]* [^\s]*')
			})
		}),

		# ETA
		validators.Object(definitions={
			'name': validators.String(enum=['eta']),
			'params': validators.Object(definitions={
				'datetime': validators.String(format='datetime')
			})
		}),

		# Countdown
		validators.Object(definitions={
			'name': validators.String(enum=['countdown']),
			'params': validators.Object(definitions={
				'seconds': validators.String(format='datetime')
			})
		}),

	])

	task = validators.Union(items=[

		# Log
		validators.Object(definitions={
			'name': validators.String(enum=['log']),
			'params': validators.Object(definitions={
				'message': validators.String(max_length=100)
			})
		}),

		# Email
		validators.Object(definitions={
			'name': validators.String(enum=['email']),
			'params': validators.Object(definitions={
				'to': validators.String(pattern=r'[^@]*@[^@]*.[^@]*'),
				'subject': validators.String(max_length=100),
				'body': validators.String(max_length=100)
			})
		}),

		# GET
		validators.Object(definitions={
			'name': validators.String(enum=['get']),
			'params': validators.Object(definitions={
				'url': validators.String(pattern='^http.*')
			})
		})
	])
