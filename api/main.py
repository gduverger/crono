import os
import falcon
import logging

from rq import Queue
from api import resources, utils
from falcon_auth import FalconAuthMiddleware, TokenAuthBackend
from postmarker.core import PostmarkClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_TOKEN = '1f40dc15-3f8c-4bfe-9e75-2d59e68350f0'
TOKENS = [TEST_TOKEN]

# Email
postmark = PostmarkClient(server_token='7be71b51-6cb1-4a7c-b1ec-21e4c1b4ec5d')

# Authentication
user_loader = lambda token: token in TOKENS
token_auth = TokenAuthBackend(user_loader)
auth_middleware = FalconAuthMiddleware(token_auth)

# API
api = falcon.API(middleware=[auth_middleware])

# Scheduler
redis_password, redis_host, redis_port = utils.parse_redis_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
scheduler = BackgroundScheduler(jobstores={'redis': RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})
print('SCHEDULER.START()')
scheduler.start()

# Routes
api.add_route('/v0/jobs', resources.Jobs())
api.add_route('/v0/jobs/{job_id}', resources.Job())

# Static
api.add_route('/', resources.Index())
api.add_static_route('/static', '{}/static'.format(DIR_PATH))

# Logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
