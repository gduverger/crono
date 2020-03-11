import redbeat
import celery

from crono import queue
from crono import utils


def timer(hours=None, minutes=None, seconds=None):
	time = utils.seconds(hours=hours, minutes=minutes, seconds=seconds)
	
	if time:
		return redbeat.schedules.rrule('SECONDLY', interval=interval, count=1, app=queue.queue) # HACK

	raise Exception('timer trigger not valid')


def datetime(datetime_):
	if datetime_:
		return redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=queue.queue) # HACK

	raise Exception('datetime trigger not valid')


def interval(hours=None, minutes=None, seconds=None):
	time = utils.seconds(hours=hours, minutes=minutes, seconds=seconds)

	if time:
		return celery.schedules.schedule(run_every=time, app=queue.queue)

	raise Exception('interval trigger not valid')


def crontab(string):
	try:
		minute, hour, day_of_week, day_of_month, month_of_year = string.split(' ')
		return celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)

	except ValueError as e:
		raise Exception('crontab trigger not valid')
