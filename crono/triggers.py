import redbeat
import celery

from crono import queue


def timer(seconds=None, minutes=None):
	interval = None

	if seconds:
		interval = seconds

	if minutes:
		interval = (interval if interval else 0) + (minutes * 60)

	if interval:
		return redbeat.schedules.rrule('SECONDLY', interval=interval, count=1, app=queue.queue)

	raise Exception('timer trigger not valid')

def datetime(datetime_):
	if datetime_:
		return redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=queue.queue) # HACK

	raise Exception('datetime trigger not valid')

def interval(seconds=None):
	if seconds:
		return celery.schedules.schedule(run_every=seconds, app=queue.queue)

	raise Exception('interval trigger not valid')

def crontab(string):
	if string:
		minute, hour, day_of_week, day_of_month, month_of_year = '0', '6', '*', '*', '2'
		return celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)

	raise Exception('crontab trigger not valid')
