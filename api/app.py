import os
import datetime
import redbeat
import celery

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import scheduler, models
from apistar import http, App, Include, Route


def index() -> str:
	return 'crono'


def test(request: http.Request, user_agent: http.Header, query_params: http.QueryParams) -> dict:
	return {
		'method': request.method,
		'url': request.url,
		'headers': dict(request.headers),
		'body': request.body.decode('utf-8'),
		'user-agent': user_agent,
		'params': dict(query_params)
	}


def get_jobs() -> list:
	return [entry.key for _, entry in scheduler._scheduler.schedule.items()]


def post_job(job: models.Job) -> str:
	schedule = None

	if job.trigger.name == 'interval':
		seconds = datetime.timedelta(seconds=int(job.trigger.value))
		schedule = celery.schedules.schedule(run_every=seconds, app=scheduler.queue)

	elif job.trigger.name == 'crontab':
		minute, hour, day_of_month, month_of_year, day_of_week = job.trigger.value.split(' ')
		schedule = celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=scheduler.queue)

	# elif job.trigger == 'date':
	# 	schedule = 

	params = {param['key']: param['value'] for param in job.task.params}
	task = 'api.tasks.{}'.format(job.task.name)
	entry = redbeat.schedulers.RedBeatSchedulerEntry(name=datetime.datetime.now().isoformat(), task=task, schedule=schedule, kwargs=params, app=scheduler.queue)
	entry.save()
	return entry.key


def get_job(key: str) -> str:
	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(key, app=scheduler.queue)
	return repr(entry)


def delete_job(key: str) -> str:
	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(key, app=scheduler.queue)
	entry.delete()
	return repr(entry)


routes = [
	Route('/', method='GET', handler=index),
	Route('/test', method='GET', handler=test),
	Route('/jobs', method='GET', handler=get_jobs),
	Route('/jobs/', method='GET', handler=get_jobs, name='get_jobs_slash'),
	Route('/jobs', method='POST', handler=post_job),
	Route('/jobs/', method='POST', handler=post_job, name='post_job_slash'),
	Route('/jobs/{key}', method='GET', handler=get_job),
	Route('/jobs/{key}/', method='GET', handler=get_job, name='get_job_slash'),
	Route('/jobs/{key}', method='DELETE', handler=delete_job),
	Route('/jobs/{key}/', method='DELETE', handler=delete_job, name='delete_job_slash'),
	# Include('/docs', docs_urls),
	# Include('/static', static_urls)
]


app = App(routes=routes)


if __name__ == '__main__':
	app.serve('127.0.0.1', 5000, debug=True)
