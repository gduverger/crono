import pytest
from apistar import exceptions, validators

foo = validators.Object(
	required=['foo'],
	properties=[
		('foo', validators.String(enum=['bar']))
	]
)

def test_validate():
	"""
	python -m pytest tests/test_apistar.py::test_validate
	"""

	with pytest.raises(exceptions.ValidationError, match="{'foo': 'The \"foo\" field is required.'}"):
		foo.validate({})

	with pytest.raises(exceptions.ValidationError, match="{'foo': 'Must be a string.'}"):
		foo.validate({'foo': []})

	with pytest.raises(exceptions.ValidationError, match="{'foo': 'Must be bar.'}"):
		foo.validate({'foo': 'err'})

	assert foo.validate({'foo': 'bar'})
