import os

from celery import Celery
# from celery.task import periodic_task


queue = Celery('scheduler',
		broker=os.getenv('REDISTOGO_URL', 'redis://localhost'), # redis://localhost:6379/0
		backend=os.getenv('REDISTOGO_URL', 'redis://localhost'),
		include=['api.tasks'])

queue.conf.redbeat_redis_url = 'redis://localhost:6379/1'
# queue.conf.beat_scheduler = 'redbeat.schedulers.RedBeatScheduler'
# queue.conf.beat_schedule = {
# 	'add-every-30-seconds': {
# 		'task': 'api.tasks.add',
# 		'schedule': 30.0,
# 		'args': (16, 16)
# 	},
# }

# @periodic_task(run_every=datetime.timedelta(seconds=10))
# def periodic_print():
# 	print('[periodic_print]')


if __name__ == '__main__':
	queue.start()
