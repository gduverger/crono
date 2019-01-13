# Crono

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

## UUID

	
	# Job key
	import uuid
	str(uuid.uuid4())

	# User token
	import secrets
	secrets.token_hex()

## Test

	python -m pytest

## Requirements

	pipenv lock -r
