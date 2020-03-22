import datetime
import redbeat
import celery

from crono import queue, utils

def timer(hours=None, minutes=None, seconds=None):
	seconds_ = utils.seconds(hours=hours, minutes=minutes, seconds=seconds)
	start = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds_)
	return redbeat.schedules.rrule(redbeat.schedules.SECONDLY, dtstart=start, count=1, app=queue.queue)

def date(datetime_):
	return redbeat.schedules.rrule(redbeat.schedules.SECONDLY, dtstart=datetime_, count=1, app=queue.queue)

def interval(hours=None, minutes=None, seconds=None):
	seconds_ = utils.seconds(hours=hours, minutes=minutes, seconds=seconds)
	return celery.schedules.schedule(run_every=seconds_, app=queue.queue)

def cron(expression):
	minute, hour, day_of_week, day_of_month, month_of_year = expression.split(' ')
	return celery.schedules.crontab(
		minute=minute,
		hour=hour,
		day_of_week=day_of_week,
		day_of_month=day_of_month,
		month_of_year=month_of_year,
		app=queue.queue)
