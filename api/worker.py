import os
import redis

from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_connection = redis.from_url(redis_url)


if __name__ == '__main__':

	with Connection(redis_connection):
		worker = Worker(map(Queue, listen))
		worker.work()
