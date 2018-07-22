import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import schemas, hooks, components, models
from apistar import http, App, Include, Route


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def get_index(app: App):
	return app.render_template('index.html', heap_analytics_id=os.getenv('HEAP_ANALYTICS_ID'))


def get_user(user: models.User) -> dict:
	return user.to_dict()


def get_jobs(user: models.User) -> list:
	return [job.to_dict() for job in user.get_jobs()]


def post_job(user: models.User, job: schemas.Job) -> dict:
	return user.add_job(job).to_dict()


def get_job(user: models.User, key: str) -> dict:
	return user.get_job(key).to_dict()


def delete_job(user: models.User, key: str) -> dict:
	return user.remove_job(key).to_dict()


routes = [
	Route('/', method='GET', handler=get_index),
	Route('/user', method='GET', handler=get_user),
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
	# NOTE the order matters
	components.AuthorizationComponent(),
]

event_hooks = [
	# NOTE the order matters
	# hooks.TimingHook(),
	hooks.AuthenticationHook(),
	# hooks.ErrorHook(),
]

app = App(routes=routes, components=components, event_hooks=event_hooks, template_dir=TEMPLATE_DIR, static_dir=STATIC_DIR)


if __name__ == '__main__':
	app.serve('127.0.0.1', 5000, debug=True)
