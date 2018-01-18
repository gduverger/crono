import os
import falcon

from rq import Queue
from api import worker, resources
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from urllib.parse import urlparse


api = falcon.API()
redis_url_parsed = urlparse(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
scheduler = BackgroundScheduler(jobstores={'redis': RedisJobStore(host=redis_url_parsed.hostname, port=redis_url_parsed.port)})
queue = Queue(connection=worker.conn)

api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
