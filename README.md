// export PATH=$PATH:/Users/gduverger/Sites/redis-4.0.6/src

redis-server &
// redis-cli shutdown
celery -A api.scheduler worker -l info &
celery -A api.scheduler beat -S redbeat.RedBeatScheduler -l info &
gunicorn api.main:api

# Scaling

	heroku ps:scale web=1 clock=1

https://stackoverflow.com/questions/32373754/apscheduler-how-to-add-job-outside-the-scheduler
https://github.com/agronholm/apscheduler/commit/19fa2fa27a7e168fbcec883817408a21a8b7339e
