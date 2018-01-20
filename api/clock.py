from api import worker, utils
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore


redis_password, redis_host, redis_port = utils.parse_redis_url(worker.redis_url)
scheduler = BlockingScheduler(jobstores={'redis': RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})


if __name__ == "__main__":
	scheduler.start()
