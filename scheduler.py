import os
import celery
import redbeat


queue = celery.Celery('crono-api', # NOTE Name of the main module if running as __main__
		broker=os.getenv('CELERY_REDIS_URL'),
		backend=os.getenv('CELERY_REDIS_URL'),
		include=['tasks'])

queue.conf.broker_pool_limit = 1
queue.conf.redis_max_connections = 1
queue.conf.redbeat_redis_url = os.getenv('REDBEAT_REDIS_URL')
# queue.conf.beat_max_loop_interval = 5
# queue.conf.redbeat_lock_timeout = 5
# queue.conf.result_backend = 'redis://localhost:6379/0'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'

_scheduler = redbeat.schedulers.RedBeatScheduler(queue, lazy=True)


if __name__ == '__main__':
	queue.start()
