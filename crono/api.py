from crono import job as _job, triggers

# Jobs

def jobs(*args, **kwargs):
	return _job.Job.jobs(*args, **kwargs)

def job(*args, **kwargs):
	return _job.Job.job(*args, **kwargs)

def meta(*args, **kwargs):
	return _job.Job.meta(*args, **kwargs)

def delete(*args, **kwargs):
	return _job.Job.delete(*args, **kwargs)

# Tasks

def log(*args, **kwargs):
	return _job.Job(task='crono.tasks.log', args=args, kwargs=kwargs)

def request(*args, **kwargs):
	return _job.Job(task='crono.tasks.request', args=args, kwargs=kwargs)

def message(*args, **kwargs):
	return _job.Job(task='crono.tasks.message', args=args, kwargs=kwargs)

def email(*args, **kwargs):
	return _job.Job(task='crono.tasks.email', args=args, kwargs=kwargs)

# Triggers

def on(*args, **kwargs):
	return _job.Job(trigger=triggers.on(*args, **kwargs))

def after(*args, **kwargs):
	return _job.Job(trigger=triggers.after(*args, **kwargs))

def every(*args, **kwargs):
	return _job.Job(trigger=triggers.every(*args, **kwargs))

def cron(*args, **kwargs):
	return _job.Job(trigger=triggers.cron(*args, **kwargs))
