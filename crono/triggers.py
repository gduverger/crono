import datetime
import redbeat
import celery

from crono import queue
from crono import utils


# TODO error handling

def timer(hours=None, minutes=None, seconds=None):
	seconds_ = utils.seconds(hours=hours, minutes=minutes, seconds=seconds)
	start = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds_)
	return redbeat.schedules.rrule(redbeat.schedules.SECONDLY, dtstart=start, count=1, app=queue.queue)


def date(_datetime):
	# now = datetime.datetime.utcnow()
	# return celery.schedules.maybe_schedule(_datetime - now, app=queue.queue)
	return redbeat.schedules.rrule(redbeat.schedules.SECONDLY, dtstart=_datetime, count=1, app=queue.queue)


def interval(hours=None, minutes=None):
	time = utils.seconds(hours=hours, minutes=minutes, seconds=0)
	return celery.schedules.schedule(run_every=time, app=queue.queue)


def cron(string):
	minute, hour, day_of_week, day_of_month, month_of_year = string.split(' ')
	return celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)


def solar(event, lat, lon):
	return celery.schedules.solar(event, lat, lon, app=queue.queue)
