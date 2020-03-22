from crono import job, triggers

# Triggers

def on(*args, **kwargs):
	return job.Job(trigger=triggers.date(*args, **kwargs))

def after(*args, **kwargs):
	return job.Job(trigger=triggers.timer(*args, **kwargs))

def every(*args, **kwargs):
	return job.Job(trigger=triggers.interval(*args, **kwargs))

def at(*args, **kwargs):
	raise Exception('`at` trigger not implemented')

def cron(*args, **kwargs):
	return job.Job(trigger=triggers.cron(*args, **kwargs))

# Tasks

def log(*args, **kwargs):
	return job.Job(task='crono.tasks.log', args=args, kwargs=kwargs)

def request(*args, **kwargs):
	return job.Job(task='crono.tasks.request', args=args, kwargs=kwargs)

def message(*args, **kwargs):
	return job.Job(task='crono.tasks.message', args=args, kwargs=kwargs)

def email(*args, **kwargs):
	return job.Job(task='crono.tasks.email', args=args, kwargs=kwargs)
