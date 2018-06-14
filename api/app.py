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
	name = job.name if hasattr(job, 'name') else datetime.datetime.now().isoformat()
	delta = datetime.timedelta(seconds=job.trigger.seconds)
	interval = celery.schedules.schedule(run_every=delta)
	params = {param['key']: param['value'] for param in job.task.params}
	entry = redbeat.schedulers.RedBeatSchedulerEntry(name=name, task=job.task.name, schedule=interval, kwargs=params, app=scheduler.queue)
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
