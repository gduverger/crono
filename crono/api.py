import logging

from crono import job
from crono import triggers

# Triggers

def on(*args, **kwargs):
	return job.Job(trigger=triggers.datetime(*args, **kwargs))

def after(*args, **kwargs):
	return job.Job(trigger=triggers.timer(*args, **kwargs))

def every(*args, **kwargs):
	return job.Job(trigger=triggers.interval(*args, **kwargs))

def at(*args, **kwargs):
	# TODO https://en.wikipedia.org/wiki/At_(command)
	raise Exception('not implemented')

def cron(*args, **kwargs):
	return job.Job(trigger=triggers.cron(*args, **kwargs))

def when(*args, **kwargs):
	return job.Job(trigger=triggers.solar(*args, **kwargs))

# Tasks

def log(*args, **kwargs):
	return job.Job(task='crono.tasks.log', args=args, kwargs=kwargs)

def request(*args, **kwargs):
	return job.Job(task='crono.tasks.request', args=args, kwargs=kwargs)

def message(*args, **kwargs):
	return job.Job(task='crono.tasks.message', args=args, kwargs=kwargs)

def email(*args, **kwargs):
	return job.Job(task='crono.tasks.email', args=args, kwargs=kwargs)
