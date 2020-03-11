redis-server &
celery worker --app=crono.queue:queue --hostname=worker1@%h --loglevel=DEBUG --detach
celery beat --app=crono.queue:queue --scheduler=redbeat.schedulers.RedBeatScheduler --loglevel=DEBUG --detach