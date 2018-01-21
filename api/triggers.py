
class Trigger(object):

	def __init__(self, params):
		self.params = {}

		for key in self.KEYS:
			if params.get(key):
				self.params[key] = params[key]

		if len(self.params) == 0:
			raise TriggerException('Missing trigger parameters')

	@staticmethod
	def init(params):
		type_ = None

		# Type
		if params.get('type'):
			type_ = params['type']
		else:
			raise TriggerException('Missing trigger type')

		# Class
		if type_ == IntervalTrigger.TYPE:
			return IntervalTrigger(params)
		elif type_ == DateTrigger.TYPE:
			return DateTrigger(params)
		elif type_ == CronTrigger.TYPE:
			return CronTrigger(params)
		else:
			raise TriggerException('Invalid trigger type')

	@property
	def type(self):
		return self.TYPE


class IntervalTrigger(Trigger):

	TYPE = 'interval'
	KEYS = (
		'weeks',
		'days',
		'hours',
		'minutes',
		'seconds',
		# 'start_date',
		# 'end_date',
		# 'timezone',
		# 'jitter'
	)


class DateTrigger(Trigger):
	
	TYPE = 'date'
	KEYS = (
		'run_date',
		# 'timezone'
	)


class CronTrigger(Trigger):
	
	TYPE = 'cron'
	KEYS = (
		'year',
		'month',
		'day',
		'week',
		'day_of_week',
		'hour',
		'minute',
		'second',
		# 'start_date',
		# 'end_date',
		# 'timezone',
		# 'jitter'
	)


class TriggerException(Exception):
	pass
