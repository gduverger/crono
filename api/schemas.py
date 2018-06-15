import typing

from apistar import types, validators

class Job(types.Type):

	trigger = validators.Union(items=[

		# Interval
		validators.Object(definitions={
			'name': validators.String(enum=['interval']),
			'arg': validators.Integer(minimum=300, default=3600) # 5 minutes, 1 hour
		}),

		#  Crontab
		validators.Object(definitions={
			'name': validators.String(enum=['crontab']),
			'arg': validators.String(pattern='[^\s]* [^\s]* [^\s]* [^\s]* [^\s]*')
		}),

		# Datetime
		validators.Object(definitions={
			'name': validators.String(enum=['datetime']),
			'arg': validators.String(format='datetime')
		})
	])

	command = validators.Union(items=[

		# Log
		validators.Object(definitions={
			'name': validators.String(enum=['log']),
			'arg': validators.String(max_length=100)
		}),

		# Email
		validators.Object(definitions={
			'name': validators.String(enum=['email']),
			# 'args': validators.Array(items=EmailCommandArgument) # TODO
		}),

		# GET
		validators.Object(definitions={
			'name': validators.String(enum=['get']),
			'arg': validators.String(pattern='^http.*')
		})
	])
