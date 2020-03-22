"""
python -m pytest tests/test_utils.py
"""

import datetime

from crono import utils
from dateutil.rrule import *


def test_seconds():
	"""
	python -m pytest tests/test_utils.py::test_seconds
	"""

	assert utils.seconds(seconds=42) == 42
	assert utils.seconds(minutes=42) == 42 * 60
	assert utils.seconds(hours=42) == 42 * 60 * 60
	assert utils.seconds(minutes=42, seconds=42) == 42 + (42 * 60)
	assert utils.seconds(hours=42, minutes=42, seconds=42) == 42 + (42 * 60) + (42 * 60 * 60)


def test_class():
	"""
	python -m pytest tests/test_utils.py::test_class
	"""

	bar = [1, 2, 3]

	class Foo:

		def __init__(self, bar=None):
			self.bar = bar

	foo = Foo(bar=bar)
	assert bar == [1, 2, 3]
	assert foo.bar == [1, 2, 3]

	bar = [4, 5, 6]
	assert bar == [4, 5, 6]
	assert foo.bar == [1, 2, 3]

	foo.bar = [7, 8, 9]
	assert bar == [4, 5, 6]
	assert foo.bar == [7, 8, 9]


def test_list():
	"""
	python -m pytest tests/test_utils.py::test_list
	"""

	assert [0, 1, 2] == [0, 1, 2]
	assert [0, 1, 2] != [2, 1, 0]

	assert all(x in [0, 1, 2] for x in [0, 1, 2])
	assert all(x in [0, 1, 2] for x in [2, 1, 0])


def test_rrule():
	"""
	python -m pytest tests/test_utils.py::test_rrule
	"""

	seconds = 60 * 60 # 1 hour
	start = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

	hourly = rrule(HOURLY, dtstart=start, count=1)
	secondly = rrule(SECONDLY, dtstart=start, count=1)

	assert len(list(hourly)) == 1
	assert len(list(secondly)) == 1

	assert hourly[0] == secondly[0]
	assert hourly[0].hour == start.hour
	assert hourly[0].minute == start.minute
	assert hourly[0].second == start.second
