# Crono

## Environmental variables
	
	# REDIS_URL
	REDIS_BROKER_URL
	REDIS_BACKEND_URL
	REDIS_MAX_CONNECTIONS

	ENVIRONMENT

## Redis

	https://redis.io/download
	// export PATH=$PATH:~/Sites/redis-4.0.6/src

	redis-server &
	// redis-cli shutdown

	heroku redis:cli
	flushall

	scan 0 match redbeat* // count 100
	hgetall {key}
	// del/hdel

## Test

	python -m pytest
