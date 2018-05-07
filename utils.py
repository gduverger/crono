import re


def dict_job(job):
	print('[dict_job] job={}'.format(job))
	return {
		'job': {
			'id': job.id,
			'name': job.name,
			'task': job.func.__name__,
			'trigger': repr(job.trigger),
			# 'params': job.kwargs # BUG
		}
	}
