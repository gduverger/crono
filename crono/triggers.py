import redbeat
import celery

def timer():
	return redbeat.schedules.rrule('SECONDLY', interval=seconds, count=1, app=queue.queue)

def datetime(datetime):
	return redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=queue.queue) # HACK

def interval():
	return celery.schedules.schedule(run_every=seconds, app=queue.queue)

def crontab(string):
	# return celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=queue.queue)
	pass

