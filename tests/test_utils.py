from api import utils


def test_parse_redis_url():
	host, port = utils.parse_redis_url('redis://localhost:6379')
	assert host == 'localhost'
	assert port == '6379'

	host, port = utils.parse_redis_url('redis://redistogo:901694911f6ab3ff06cbb55304673b50@soldierfish.redistogo.com:10460/')
	assert host == 'redistogo:901694911f6ab3ff06cbb55304673b50@soldierfish.redistogo.com'
	assert port == '10460'
