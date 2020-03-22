# Crono

## Environmental variables
	
	REDIS_URL
	REDIS_BROKER_URL
	REDIS_BACKEND_URL
	REDIS_MAX_CONNECTIONS
	REDIS_MAX_CONNECTIONS (default: 20)
	BEAT_MAX_LOOP_INTERVAL (default: 300)
	BROKER_POOL_LIMIT (default: None)
	TASK_IGNORE_RESULT (default: True)
	WORKER_MAX_TASKS_PER_CHILD (default: 100)

## How to start

	redis-server &
	celery worker --app=crono.queue:queue --hostname=worker1@%h --loglevel=DEBUG
	celery beat --app=crono.queue:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG

## How to stop

	redis-cli flushall
	redis-cli shutdown

## How to test

	python -m pytest
