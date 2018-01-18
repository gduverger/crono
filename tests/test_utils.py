from api import utils


def test_parse_redis_url():
	password, host, port = utils.parse_redis_url('redis://localhost:6379')
	assert password == None
	assert host == 'localhost'
	assert port == '6379'

	password, host, port = utils.parse_redis_url('redis://redistogo:901694911f6ab3ff06cbb55304673b50@soldierfish.redistogo.com:10460/')
	assert password == '901694911f6ab3ff06cbb55304673b50'
	assert host == 'soldierfish.redistogo.com'
	assert port == '10460'
