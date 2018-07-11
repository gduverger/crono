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

# Scale

	heroku ps:scale web=1 clock=1

# Logs

	heroku drains:add https://<TIMBER_API_KEY>@logs.timber.io/frames --app=crono-stag
