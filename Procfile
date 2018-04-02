worker: celery worker --app=scheduler:queue --concurrency=1 --loglevel=INFO
clock: celery beat --app=scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=INFO
web: gunicorn app:app --workers=1
