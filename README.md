# Crono

## Environmental variables
	
	# REDIS_URL
	REDIS_BROKER_URL
	REDIS_BACKEND_URL
	REDIS_MAX_CONNECTIONS

## How to start

	redis-server &
	celery worker --app=crono.queue:queue --hostname=worker1@%h --loglevel=DEBUG
	celery beat --app=crono.queue:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG

## How to stop

	redis-cli shutdown

## How to test

	python -m pytest
