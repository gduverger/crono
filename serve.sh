redis-server &
celery worker --app=crono.queue:queue --loglevel=DEBUG --detach
celery beat --app=crono.queue:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach