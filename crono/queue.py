import os
import celery

# NOTE
# Name of the main module if running as __main__.
# This is used as the prefix for auto-generated task names.
queue = celery.Celery('crono')

queue.conf.include = ['crono.tasks']
queue.conf.broker_url = os.getenv('CELERY_BROKER')
queue.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND')
queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'
queue.conf.broker_pool_limit = int(os.getenv('CELERY_BROKER_POOL_LIMIT', 0))
queue.conf.task_ignore_result = bool(os.getenv('CELERY_TASK_IGNORE_RESULT', True))
queue.conf.beat_max_loop_interval = int(os.getenv('CELERY_BEAT_MAX_LOOP_INTERVAL', 300))

# NOTE
# Heroku Redis' Hobby Dev has a limit of 20 connections
# https://elements.heroku.com/addons/heroku-redis
queue.conf.redis_max_connections = int(os.getenv('REDIS_MAX_CONNECTIONS', 20))

# NOTE
# Celery seems to have a memory leak with redis broker
# http://docs.celeryproject.org/en/3.1/configuration.html#celeryd-max-tasks-per-child
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#worker-max-memory-per-child
queue.conf.worker_max_tasks_per_child = int(os.getenv('CELERY_WORKER_MAX_TASKS_PER_CHILD', 100))

if __name__ == '__main__':
	queue.start()
