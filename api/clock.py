import os
import re

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore


# DUPLICATE utils.py
def parse_redis_url(url):
	password = None
	host = None
	port = None
	match = re.search('^redis://([a-z0-9.@:]+):([0-9]+)/?$', url)

	if match:
		host = match.group(1)
		port = match.group(2)

		_match = re.search('^[a-z]+:([a-z0-9]+)@([a-z.]+)$', host)
		if _match:
			password = _match.group(1)
			host = _match.group(2)

	return password, host, port


redis_password, redis_host, redis_port = parse_redis_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
scheduler = BlockingScheduler(jobstores={'redis': RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})


if __name__ == '__main__':
	scheduler.start()
