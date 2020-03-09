redis-server &
celery worker --app=crono.scheduler:queue --loglevel=DEBUG --detach
celery beat --app=crono.scheduler:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach