import os
import sys
import rpyc

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api import utils

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from rpyc.utils.server import ThreadedServer
from apscheduler.jobstores.base import JobLookupError


JOBSTORE = 'redis'


class SchedulerService(rpyc.Service):

	def exposed_get_jobs(self):
		print('[exposed_get_jobs] self={}'.format(self))
		return scheduler.get_jobs(jobstore=JOBSTORE)

	def exposed_add_job(self, func, *args, **kwargs):
		print('[exposed_add_job] self={} func={} args={} kwargs={}'.format(self, func, args, kwargs))
		return scheduler.add_job(func, jobstore=JOBSTORE, *args, **kwargs)

	# def exposed_remove_all_jobs(self):
	# 	print('[exposed_remove_all_jobs] self={}'.format(self))
	# 	scheduler.remove_all_jobs(jobstore=JOBSTORE)

	def exposed_get_job(self, job_id):
		print('[exposed_get_job] self={} job_id={}'.format(self, job_id))
		return scheduler.get_job(job_id, jobstore=JOBSTORE)

	def exposed_remove_job(self, job_id):
		print('[exposed_remove_job] self={} job_id={}'.format(self, job_id))
		try:
			scheduler.remove_job(job_id, jobstore=JOBSTORE)
		except JobLookupError as e:
			# TODO exception handling
			pass


if __name__ == '__main__':

	redis_password, redis_host, redis_port = utils.parse_redis_url(os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))
	scheduler = BackgroundScheduler(jobstores={JOBSTORE: RedisJobStore(host=redis_host, port=redis_port, password=redis_password)})
	scheduler.start()
	protocol_config = {'allow_all_attrs': True}
	server = ThreadedServer(SchedulerService, hostname='localhost', port=12345, protocol_config=protocol_config)

	try:
		server.start()

	except (KeyboardInterrupt, SystemExit):
		pass

	finally:
		scheduler.shutdown()
