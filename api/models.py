from apistar import types, validators


class Parameter(types.Type):
	key = validators.String(enum=['to', 'message', 'subject', 'body', 'url'])
	value = validators.String(max_length=100)


class Trigger(types.Type):
	name = validators.String(enum=['interval', 'crontab']) # 'date'
	value = validators.String(max_length=100)


class Task(types.Type):
	name = validators.String(enum=['log', 'email', 'get'])
	params = validators.Array(items=Parameter)


class Job(types.Type):
	trigger = Trigger
	task = Task
