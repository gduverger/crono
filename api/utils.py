import re

def parse_redis_url(url):
	match = re.search('^redis://([a-z0-9:@.]*):([0-9]*)/?$', url)
	return match.group(1), match.group(2)
