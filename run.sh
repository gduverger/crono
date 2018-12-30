# . run.sh
redis-server &
celery worker --app=api.scheduler:queue --loglevel=DEBUG --detach
celery beat --app=api.scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach
gunicorn api.app:app --bind=127.0.0.1:5000
