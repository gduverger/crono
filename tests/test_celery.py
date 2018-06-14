from celery import schedules as celery_schedules

"""
python -m pytest tests/test_celery.py::TestCelery
"""

class TestCelery(object):

	def test_crontab_parser(self):
		"""
		python -m pytest tests/test_celery.py::TestCelery::test_crontab_parser
		"""
		assert celery_schedules.crontab_parser(60).parse('*/15') == {0, 45, 30, 15}
		assert celery_schedules.crontab_parser().parse('*/15') == {0, 45, 30, 15}
		assert celery_schedules.crontab_parser().parse('0 6 * * *') == True


	def test_crontab(self):
		"""
		python -m pytest tests/test_celery.py::TestCelery::test_crontab
		"""
		assert celery_schedules.crontab(run_every='0 6 * * *') == True