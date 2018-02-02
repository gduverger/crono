from celery import Celery


queue = Celery('queue',
		broker='redis://localhost:6379/0', # redis://:password@hostname:port/db_number
		include=['api.commands'])
# app.conf.result_backend = 'redis://localhost:6379/0'


class SchedulerService(): # rpyc.Service

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
	queue.start()
