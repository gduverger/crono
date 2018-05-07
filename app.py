import os
import datetime
import scheduler
import redbeat
import celery

from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import typesystem

from postmarker.core import PostmarkClient


def welcome(name=None):
	if name is None:
		return {'message': 'Welcome to Crono!'}
	return {'message': 'Welcome to Crono, %s!' % name}


class Trigger(typesystem.Object):
	description = 'Trigger'
	properties = {
		'type': typesystem.enum(enum=['interval']), # 'date', 'cron'
		'seconds': typesystem.integer(minimum=10, default=60)
	}
	required = ['type', 'seconds']


class TaskParameters(typesystem.Object):
	properties = {
		'to': typesystem.string(pattern='.*@.*'),
		# 'subject': typesystem.string(max_length=100),
		'body': typesystem.string(max_length=100, default='hello')
	}


class Task(typesystem.Object):
	description = 'Task'
	properties = {
		'type': typesystem.enum(enum=['log', 'email']),
		'parameters': TaskParameters
	}
	required = ['type', 'parameters']


class Job(typesystem.Object):
	description = 'Job'
	properties = {
		'name': typesystem.string(max_length=100),
		'trigger': Trigger,
		'task': Task,
	}
	required = ['trigger', 'task']


def get_jobs():
	return [entry.key for _, entry in scheduler._scheduler.schedule.items()]


def post_job(job: Job):
	name = job['name'] if hasattr(job, 'name') else str(datetime.datetime.now())
	interval = celery.schedules.schedule(run_every=job['trigger']['seconds']) # seconds
	entry = redbeat.schedulers.RedBeatSchedulerEntry(name=name, task=job['task']['type'], schedule=interval, kwargs=job['task']['parameters'], app=scheduler.queue)
	entry.save()

	return entry.key


def get_job(job_id: str):
	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(job_id, app=scheduler.queue)
	return repr(entry)


def delete_job(job_id: str):
	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(job_id, app=scheduler.queue)
	entry.delete()
	return repr(entry)


routes = [
	Route('/', 'GET', welcome),
	Route('/jobs', 'GET', get_jobs),
	Route('/jobs/', 'GET', get_jobs, name='get_jobs_slash'),
	Route('/jobs', 'POST', post_job),
	Route('/jobs/', 'POST', post_job, name='post_job_slash'),
	Route('/jobs/{job_id}', 'GET', get_job),
	Route('/jobs/{job_id}/', 'GET', get_job, name='get_job_slash'),
	Route('/jobs/{job_id}', 'DELETE', delete_job),
	Route('/jobs/{job_id}/', 'DELETE', delete_job, name='delete_job_slash'),
	Include('/docs', docs_urls),
	Include('/static', static_urls)
]


app = App(routes=routes)


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


if __name__ == '__main__':
	app.main()
