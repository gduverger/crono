import os
import celery
import redbeat


queue = celery.Celery('api',
		broker=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
		backend=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
		include=['api.tasks'])

queue.conf.redis_max_connections = 5
queue.conf.broker_pool_limit = 5
queue.conf.redbeat_redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379/1')

# queue.conf.beat_max_loop_interval = 5
# queue.conf.redbeat_lock_timeout = 5
# queue.conf.result_backend = 'redis://localhost:6379/0'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'

_scheduler = redbeat.schedulers.RedBeatScheduler(queue, lazy=True)


if __name__ == '__main__':
	queue.start()
