import re

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


def dict_job(job):
	print('[dict_job] job={}'.format(job))
	return {
		'job': {
			'id': job.id,
			'name': job.name,
			'command': job.func.__name__,
			'trigger': repr(job.trigger),
			# 'params': job.kwargs # BUG
		}
	}
