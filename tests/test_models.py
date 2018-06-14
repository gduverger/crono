from api import models

"""
python -m pytest tests/test_models.py::TestModels
"""

class TestModels(object):

	def test_trigger(self):
		"""
		python -m pytest tests/test_models.py::TestModels::test_trigger
		"""
		trigger = models.Trigger({'name': 'interval'})
		assert dict(trigger) == {'name': 'interval', 'seconds': 60}
		assert trigger['name'] == 'interval'
		assert trigger.name == 'interval'
