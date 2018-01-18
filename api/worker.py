import os
import redis

from rq import Worker, Queue, Connection


listen = ['high', 'default', 'low']
conn = redis.from_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))


if __name__ == '__main__':

	with Connection(conn):
		worker = Worker(map(Queue, listen))
		worker.work()
