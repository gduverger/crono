web: gunicorn api.main:api
clock: celery -A api.scheduler beat -S redbeat.RedBeatScheduler -l info
worker: celery -A api.scheduler worker -l info
