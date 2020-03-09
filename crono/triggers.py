import redbeat
import celery

from crono import queue


def timer(seconds):
	return redbeat.schedules.rrule('SECONDLY', interval=seconds, count=1, app=queue.queue)  # HACK

def datetime(datetime_):
	return redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=queue.queue) # HACK

def interval(seconds):
	return celery.schedules.schedule(run_every=seconds, app=queue.queue)

def crontab(string):
	minute, hour, day_of_week, day_of_month, month_of_year = '0', '6', '*', '*', '2'
	return celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)

