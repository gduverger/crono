redis-server &
celery worker --app=api.scheduler:queue --loglevel=DEBUG --detach
celery beat --app=api.scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach
python api/app.py
