import pytest

from api import triggers


def test_init_exception():

	with pytest.raises(triggers.TriggerException):
		triggers.Trigger.init({})

	with pytest.raises(triggers.TriggerException):
		triggers.Trigger.init({'type': None})

	with pytest.raises(triggers.TriggerException):
		triggers.Trigger.init({'type': 'test'})

	with pytest.raises(triggers.TriggerException):
		triggers.Trigger.init({'type': 'interval'})


def test_init_interval():
	trigger = triggers.Trigger.init({'type': 'interval', 'weeks': 1})
	assert type(trigger) == triggers.IntervalTrigger
	assert trigger.type == 'interval'
	assert trigger.params == {'weeks': 1}

	trigger = triggers.Trigger.init({'type': 'interval', 'weeks': 1, 'test': None})
	assert type(trigger) == triggers.IntervalTrigger
	assert trigger.type == 'interval'
	assert trigger.params == {'weeks': 1}

	trigger = triggers.Trigger.init({'type': 'interval', 'weeks': 1, 'test': None, 'days': 2})
	assert type(trigger) == triggers.IntervalTrigger
	assert trigger.type == 'interval'
	assert trigger.params == {'weeks': 1, 'days': 2}
