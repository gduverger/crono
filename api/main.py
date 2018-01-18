import os
import falcon

from rq import Queue
from api import worker, resources
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore


api = falcon.API()
redis_kwargs = worker.redis_connection.connection_pool.connection_kwargs
scheduler = BackgroundScheduler(jobstores={'redis': RedisJobStore(host=redis_kwargs.get('host'), port=redis_kwargs.get('port'))})
queue = Queue(connection=worker.redis_connection)

api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
