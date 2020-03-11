import os
import celery
import redbeat


queue = celery.Celery('crono', # DOC Name of the main module if running as __main__. This is used as the prefix for auto-generated task names.
		broker=os.getenv('REDIS_BROKER_URL'),
		backend=os.getenv('REDIS_BACKEND_URL'),
		include=['crono.tasks'])

# queue.conf.redbeat_redis_url = os.getenv('REDIS_URL')
queue.conf.beat_max_loop_interval = os.getenv('BEAT_MAX_LOOP_INTERVAL') # in seconds
# queue.conf.redbeat_lock_timeout = 5

# NOTE Heroku Redis' Hobby Dev has a limit of 20 connections
# https://elements.heroku.com/addons/heroku-redis
queue.conf.redis_max_connections = int(os.getenv('REDIS_MAX_CONNECTIONS', 20))
queue.conf.broker_pool_limit = None
queue.conf.task_ignore_result = True

# NOTE Celery seems to have a memory leak with redis broker
# http://docs.celeryproject.org/en/3.1/configuration.html#celeryd-max-tasks-per-child
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-max-memory-per-child
queue.conf.worker_max_tasks_per_child = 100

# queue.conf.result_backend = 'redis://localhost:6379/0'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'

# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True

if __name__ == '__main__':
	queue.start()
