import redbeat
import celery

from crono import queue
from crono import utils


# TODO error handling

def timer(hours=None, minutes=None):
	time = utils.seconds(hours=hours, minutes=minutes, seconds=0)
	return celery.schedules.maybe_schedule(time, app=queue.queue)
	# return redbeat.schedules.rrule('SECONDLY', interval=time, count=1, app=queue.queue) # HACK


def datetime(datetime_):
	now = datetime.datetime.utcnow()
	return celery.schedules.maybe_schedule(datetime_ - now, app=queue.queue)
	# return redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=queue.queue) # HACK


def interval(hours=None, minutes=None):
	time = utils.seconds(hours=hours, minutes=minutes, seconds=0)
	return celery.schedules.schedule(run_every=time, app=queue.queue)


def cron(string):
	minute, hour, day_of_week, day_of_month, month_of_year = string.split(' ')
	return celery.schedules.cron(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)


def solar(event, lat, lon):
	return celery.schedules.solar(event, lat, lon, app=queue.queue)
