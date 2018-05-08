
# Install

## Redis

	https://redis.io/download
	// export PATH=$PATH:~/Sites/redis-4.0.6/src

# Run

	redis-server &
	// redis-cli shutdown

	celery worker --app=scheduler:queue --concurrency=1 --loglevel=DEBUG --detach
	celery beat --app=scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach

	gunicorn app:app --workers=1

# Test

	pytest

# Scale

	heroku ps:scale web=1 clock=1

https://stackoverflow.com/questions/32373754/apscheduler-how-to-add-job-outside-the-scheduler
https://github.com/agronholm/apscheduler/commit/19fa2fa27a7e168fbcec883817408a21a8b7339e
