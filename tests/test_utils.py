from api import utils


def test_parse_redis_url():
	password, host, port = utils.parse_redis_url('redis://localhost:6379')
	assert password == None
	assert host == 'localhost'
	assert port == '6379'

	password, host, port = utils.parse_redis_url('redis://redistogo:4913f6ab1ff06cb673b7b55304090169@soldierbowl.redistogo.com:46210/')
	assert password == '4913f6ab1ff06cb673b7b55304090169'
	assert host == 'soldierbowl.redistogo.com'
	assert port == '46210'
