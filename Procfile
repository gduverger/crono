web: gunicorn api.main:api
clock: celery -A api.scheduler beat -l info
worker: celery -A api.scheduler worker -l info
