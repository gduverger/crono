from apistar import types, validators


class Trigger(types.Type):
	name = validators.String(enum=['interval']), # 'date', 'cron'
	seconds = validators.Integer(minimum=10, default=60) # required=True


class Parameter(types.Type):
	key = validators.String(enum=['to', 'message', 'subject', 'body'])
	value = validators.String(max_length=100)


class Task(types.Type):
	name = validators.String(enum=['log', 'email'])
	params = validators.Array(items=Parameter)


class Job(types.Type):
	trigger = Trigger
	task = Task
