worker: celery worker --app=api.scheduler:queue --concurrency=1 --loglevel=INFO
clock: celery beat --app=api.scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=INFO
web: gunicorn doc.app:app --workers=1
web: gunicorn api.app:app --workers=1
