# Crono

## Environmental variables
	
	REDIS_MAX_CONNECTIONS (default: 20)	
	CELERY_BROKER
	CELERY_RESULT_BACKEND
	CELERY_BROKER_POOL_LIMIT (default: 0)
	CELERY_TASK_IGNORE_RESULT (default: True)
	CELERY_BEAT_MAX_LOOP_INTERVAL (default: 300)
	CELERY_WORKER_MAX_TASKS_PER_CHILD (default: 100)

## How to start

	redis-server &
	celery worker --app=crono.queue:queue --hostname=worker1@%h --loglevel=DEBUG
	celery beat --app=crono.queue:queue --loglevel=DEBUG

## How to stop

	redis-cli flushall
	redis-cli shutdown

## How to test

	python -m pytest

## Runtime

	python-3.7
