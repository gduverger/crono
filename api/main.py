import os
import falcon

from rq import Queue
from api import worker, resources, utils
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from falcon_auth import FalconAuthMiddleware, TokenAuthBackend


TOKENS = [
	'1f40dc15-3f8c-4bfe-9e75-2d59e68350f0'
]


# Authentication
user_loader = lambda token: token in TOKENS
token_auth = TokenAuthBackend(user_loader, auth_header_prefix='Bearer')
auth_middleware = FalconAuthMiddleware(token_auth)

api = falcon.API(middleware=[auth_middleware])

# Scheduler & Queue
redis_password, redis_host, redis_port = utils.parse_redis_url(worker.redis_url)
scheduler = BackgroundScheduler(jobstores={'redis': RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})
queue = Queue(connection=worker.redis_connection)

# Routes
api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
