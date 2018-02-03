import os

from celery import Celery


queue = Celery('scheduler',
		broker=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
		include=['api.tasks'])
# app.conf.result_backend = 'redis://localhost:6379/0'


if __name__ == '__main__':
	queue.start()
