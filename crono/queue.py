import os
import celery
import redbeat

# NOTE
# Name of the main module if running as __main__.
# This is used as the prefix for auto-generated task names.
queue = celery.Celery('crono',
	broker=os.getenv('REDIS_BROKER_URL'),
	backend=os.getenv('REDIS_BACKEND_URL'),
	include=['crono.tasks'])

# RedBeat config

# queue.conf.redbeat_redis_url = os.getenv('REDIS_URL')
# queue.conf.redbeat.redbeat_redis_use_ssl
# queue.conf.redbeat_key_prefix
# queue.conf.redbeat_lock_key
# queue.conf.redbeat_lock_timeout = 5

# Celery config

# queue.conf.result_backend = 'redis://localhost:6379/0'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'

# NOTE Heroku Redis' Hobby Dev has a limit of 20 connections
# https://elements.heroku.com/addons/heroku-redis
queue.conf.redis_max_connections = int(os.getenv('REDIS_MAX_CONNECTIONS', 20))

# NOTE Celery seems to have a memory leak with redis broker
# http://docs.celeryproject.org/en/3.1/configuration.html#celeryd-max-tasks-per-child
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-max-memory-per-child
queue.conf.worker_max_tasks_per_child = int(os.getenv('WORKER_MAX_TASKS_PER_CHILD', 100))
queue.conf.broker_pool_limit = os.getenv('BROKER_POOL_LIMIT', None)
queue.conf.task_ignore_result = os.getenv('TASK_IGNORE_RESULT', True)
queue.conf.beat_max_loop_interval = int(os.getenv('BEAT_MAX_LOOP_INTERVAL', 300)) # in seconds (5 minutes by default)

# CELERY_TIMEZONE = 'UTC'
# CELERY_ENABLE_UTC = True

if __name__ == '__main__':
	queue.start()
