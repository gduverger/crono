import os
import redis
import stripe
import datetime
import dateparser
import redbeat
import celery

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import scheduler, schemas, hooks, components
from apistar import http, App, Include, Route


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def get_index(app: App, msg: str=None):
	return app.render_template('index.html', heap_analytics_id=os.getenv('HEAP_ANALYTICS_ID'), message=msg)


def post_index(app: App):
	return get_index(app, msg='POST')


def get_test(request: http.Request, user_agent: http.Header, query_params: http.QueryParams) -> dict:
	return {
		'method': request.method,
		'url': request.url,
		'headers': dict(request.headers),
		'body': request.body.decode('utf-8'),
		'user-agent': user_agent,
		'params': dict(query_params)
	}


def get_redis(key: str=None):
	r = redis.from_url(os.getenv('REDIS_URL')) # db=0

	if key:
		t = r.type(key).decode('utf-8')

		if t == 'hash':
			# e.g., crono:2018-06-17T09:30:37.555291
			return [{k.decode('utf-8'): v.decode('utf-8')} for k, v in r.hgetall(key).items()]

		elif t == 'zset':
			# e.g., crono::schedule
			return [k.decode('utf-8') for k in r.zrange(key, 0, 2)]

	else:
		return [key.decode('utf-8') for key in r.scan_iter()]


def get_charge(app: App):
	context = {
		'stripe_amount': 1000, # in cents
		'stripe_public_key': os.getenv('STRIPE_PUBLIC_KEY'),
		'stripe_name': 'Crono',
		'stripe_description': 'Web-hosted API replacement for cron',
		'stripe_image': 'https://stripe.com/img/documentation/checkout/marketplace.png',
		'stripe_locale': 'auto',
		'stripe_zip_code': 'true',
		'heap_analytics_id': os.getenv('HEAP_ANALYTICS_ID')
	}
	return app.render_template('charge.html', **context)


def post_charge(app: App):
	# Set your secret key: remember to change this to your live secret key in production
	# See your keys here: https://dashboard.stripe.com/account/apikeys
	stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

	# Token is created using Checkout or Elements!
	# Get the payment token ID submitted by the form:
	token = request.form['stripeToken'] # Using Flask

	charge = stripe.Charge.create(
		amount=999,
		currency='usd',
		description='Example charge',
		source=token,
	)
	return app.render_template('charge.html')


def get_jobs(user: components.User) -> dict:
	i = scheduler.queue.control.inspect()
	return {
		'registered': i.registered(),
		'active': i.active(),
		'scheduled': i.scheduled(),
		'reserved': i.reserved()
	}


def post_job(job: schemas.Job) -> str:
	schedule = None

	if job.trigger['name'] == 'interval':
		seconds = datetime.timedelta(seconds=job.trigger['params']['seconds'])
		schedule = celery.schedules.schedule(run_every=seconds, app=scheduler.queue)

	elif job.trigger['name'] == 'crontab':
		minute, hour, day_of_month, month_of_year, day_of_week = job.trigger['params']['expression'].split(' ')
		schedule = celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=scheduler.queue)

	elif job.trigger['name'] == 'eta':
		# datetime_ = dateparser.parse(job.trigger['params']['datetime'])
		# schedule = redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=scheduler.queue) # HACK
		raise Exception('Not implemented yet')

	elif job.trigger['name'] == 'countdown':
		# seconds = job.trigger['params']['seconds']
		# schedule = redbeat.schedules.rrule('SECONDLY', interval=seconds, count=1, app=scheduler.queue)
		raise Exception('Not implemented yet')

	params = job.task['params']
	task = 'api.tasks.{}'.format(job.task['name'])
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
	Route('/', method='GET', handler=get_index),
	Route('/', method='POST', handler=post_index),
	Route('/test', method='GET', handler=get_test),
	Route('/redis', method='GET', handler=get_redis),
	# Route('/charge', method='GET', handler=get_charge),
	# Route('/charge', method='POST', handler=post_charge),
	Route('/jobs', method='GET', handler=get_jobs),
	Route('/jobs', method='POST', handler=post_job),
	Route('/jobs/{key}', method='GET', handler=get_job),
	Route('/jobs/{key}', method='DELETE', handler=delete_job),
	# TODO
	# Route('/logs', method='GET', handler=get_logs),

	# Include('/docs', docs_urls),
	# Include('/static', static_urls)
]


components = [
	components.UserComponent(),
]

event_hooks = [
	hooks.TimingHook(),
	hooks.AuthenticationHook(),
	hooks.ErrorHook(),
]

app = App(routes=routes, components=components, event_hooks=event_hooks, template_dir=TEMPLATE_DIR, static_dir=STATIC_DIR)


if __name__ == '__main__':
	app.serve('127.0.0.1', 5000, debug=True)
