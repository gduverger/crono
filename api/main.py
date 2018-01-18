import os
import falcon

from rq import Queue
from api import worker, resources, utils
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore


api = falcon.API()
redis_password, redis_host, redis_port = utils.parse_redis_url(worker.redis_url)
scheduler = BackgroundScheduler(jobstores={'redis': RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})
queue = Queue(connection=worker.redis_connection)

api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
