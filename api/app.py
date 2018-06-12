import os
import datetime
import redbeat
import celery

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import scheduler
from apistar import App, Include, Route
from apistar import exceptions, types, validators
from postmarker.core import PostmarkClient


def index():
	return {'hello': 'world'}


class Trigger(types.Type):
	description = 'Trigger'
	properties = {
		'type': validators.String(enum=['interval']), # 'date', 'cron'
		'seconds': validators.Integer(minimum=10, default=60)
	}
	required = ['type', 'seconds']


class TaskParameters(types.Type):
	properties = {
		'to': validators.String(pattern='.*@.*'),
		# 'subject': types.string(max_length=100),
		'body': validators.String(max_length=100, default='hello')
	}


class Task(types.Type):
	description = 'Task'
	properties = {
		'type': validators.String(enum=['log', 'email']),
		'parameters': TaskParameters
	}
	required = ['type', 'parameters']


class Job(types.Type):
	description = 'Job'
	properties = {
		'name': validators.String(max_length=100),
		'trigger': Trigger,
		'task': Task,
	}
	required = ['trigger', 'task']


def get_jobs():
	return [entry.key for _, entry in scheduler._scheduler.schedule.items()]


def post_job(job: Job):
	name = job['name'] if 'name' in job else str(datetime.datetime.now())
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
	Route('/', 'GET', index),
	Route('/jobs', 'GET', get_jobs),
	Route('/jobs/', 'GET', get_jobs, name='get_jobs_slash'),
	Route('/jobs', 'POST', post_job),
	Route('/jobs/', 'POST', post_job, name='post_job_slash'),
	Route('/jobs/{job_id}', 'GET', get_job),
	Route('/jobs/{job_id}/', 'GET', get_job, name='get_job_slash'),
	Route('/jobs/{job_id}', 'DELETE', delete_job),
	Route('/jobs/{job_id}/', 'DELETE', delete_job, name='delete_job_slash'),
	# Include('/docs', docs_urls),
	# Include('/static', static_urls)
]


app = App(routes=routes)
postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


if __name__ == '__main__':
	app.serve('127.0.0.1', 5000, debug=True)
