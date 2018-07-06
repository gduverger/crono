import os
import celery
import redbeat


queue = celery.Celery('api', # NOTE Name of the main module if running as __main__
		broker=os.getenv('REDIS_URL'),
		backend=os.getenv('REDIS_URL'),
		include=['api.tasks'])

queue.conf.redbeat_redis_url = os.getenv('REDIS_URL')
queue.conf.redis_max_connections = 18
# queue.conf.broker_pool_limit = 1
# queue.conf.beat_max_loop_interval = 5
# queue.conf.redbeat_lock_timeout = 5
# queue.conf.result_backend = 'redis://localhost:6379/0'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'

# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True

if __name__ == '__main__':
	queue.start()
