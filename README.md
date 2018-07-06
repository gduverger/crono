# Redis

	https://redis.io/download
	// export PATH=$PATH:~/Sites/redis-4.0.6/src

	redis-server &
	// redis-cli shutdown

	heroku redis:cli
	flushall

# Test

	python -m pytest

# Scale

	heroku ps:scale web=1 clock=1
