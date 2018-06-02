
# Install

## Redis

	https://redis.io/download
	// export PATH=$PATH:~/Sites/redis-4.0.6/src

	redis-server &
	// redis-cli shutdown

# Test

	python -m pytest

# Scale

	heroku ps:scale web=1 clock=1

https://stackoverflow.com/questions/32373754/apscheduler-how-to-add-job-outside-the-scheduler
https://github.com/agronholm/apscheduler/commit/19fa2fa27a7e168fbcec883817408a21a8b7339e
