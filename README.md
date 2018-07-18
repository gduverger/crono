[![Build Status](https://semaphoreci.com/api/v1/projects/6f456841-4428-4dcd-ad8c-f7034330b7de/2099247/badge.svg)](https://semaphoreci.com/gduverger-65/crono)

# Redis

	https://redis.io/download
	// export PATH=$PATH:~/Sites/redis-4.0.6/src

	redis-server &
	// redis-cli shutdown

	heroku redis:cli
	flushall

	scan 0 match redbeat* // count 100
	hgetall {key}
	// del/hdel

# Test

	python -m pytest

# Requirements

	pipenv lock -r
