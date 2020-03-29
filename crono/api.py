from crono import job as job_, triggers

# Triggers

def on(*args, **kwargs):
	return job_.Job(trigger=triggers.on(*args, **kwargs))

def after(*args, **kwargs):
	return job_.Job(trigger=triggers.after(*args, **kwargs))

def every(*args, **kwargs):
	return job_.Job(trigger=triggers.every(*args, **kwargs))

def cron(*args, **kwargs):
	return job_.Job(trigger=triggers.cron(*args, **kwargs))

def at(*args, **kwargs):
	return job_.Job(trigger=triggers.at(*args, **kwargs))

# Tasks

def log(*args, **kwargs):
	return job_.Job(task='crono.tasks.log', args=args, kwargs=kwargs)

def request(*args, **kwargs):
	return job_.Job(task='crono.tasks.request', args=args, kwargs=kwargs)

def message(*args, **kwargs):
	return job_.Job(task='crono.tasks.message', args=args, kwargs=kwargs)

def email(*args, **kwargs):
	return job_.Job(task='crono.tasks.email', args=args, kwargs=kwargs)

# Jobs

def jobs(*args, **kwargs):
	return job_.Job.jobs(*args, **kwargs)

def job(*args, **kwargs):
	return job_.Job.job(*args, **kwargs)
