from crono import job
from crono import triggers

# Triggers

def on(datetime):
	return job.Job(trigger=triggers.datetime(datetime))

def in_(**kwargs):
	return job.Job(trigger=triggers.timer(**kwargs))

def every(**kwargs):
	return job.Job(trigger=triggers.interval(**kwargs))

def at(string):
	return job.Job(trigger=triggers.crontab(string))

# Tasks

def log(string):
	return job.Job(task='crono.tasks.log')

def request():
	return job.Job(task='crono.tasks.request')

def message(text):
	return job.Job(task='crono.tasks.message')

def email():
	return job.Job(task='crono.tasks.email')

def run():
	return job.Job(task='crono.tasks.run')
