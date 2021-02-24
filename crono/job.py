import os
import uuid
import redis
import redbeat
import logging

from crono import queue, triggers

class Job:

	def __init__(self, trigger=None, task=None, args=None, kwargs=None):
		self.trigger = trigger
		self.task = task
		self.args = args
		self.kwargs = kwargs
		self.entry = None

	def save(self):

		if self.entry == None and self.task != None and self.trigger != None:
			self.name = str(uuid.uuid4())
			self.entry = redbeat.schedulers.RedBeatSchedulerEntry(name=self.name, task=self.task, schedule=self.trigger, args=self.args, kwargs=self.kwargs, app=queue.queue)
			self.entry.save()
			logging.debug(self.entry)

		return self

	# Jobs

	@classmethod
	def jobs(cls):

		# BUG
		# scheduler = redbeat.schedulers.RedBeatScheduler(app=queue.queue)
		# return scheduler.schedule

		# HACK
		# https://github.com/sibson/redbeat/issues/155
		redis = redbeat.schedulers.get_redis(queue.queue)
		conf = redbeat.schedulers.RedBeatConfig(queue.queue)
		keys = redis.zrange(conf.schedule_key, 0, -1)
		return [redbeat.schedulers.RedBeatSchedulerEntry.from_key(key, app=queue.queue) for key in keys]

	@classmethod
	def job(cls, key):

		try:
			return redbeat.schedulers.RedBeatSchedulerEntry.from_key(key, app=queue.queue)

		except KeyError:
			return None

	@classmethod
	def meta(cls, key):
		return redbeat.schedulers.RedBeatSchedulerEntry.load_meta(key, app=queue.queue)

	@classmethod
	def delete(cls, key):
		# DOC http://docs.celeryproject.org/en/latest/faq.html#can-i-cancel-the-execution-of-a-task
		# queue.queue.control.revoke(task_id)
		entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(key, app=queue.queue)
		entry.delete()
		return entry

	# Tasks

	def log(self, *args, **kwargs):
		self.task = 'crono.tasks.log'
		self.args = args
		self.kwargs = kwargs
		return self.save()

	def request(self, *args, **kwargs):
		self.task = 'crono.tasks.request'
		self.args = args
		self.kwargs = kwargs
		return self.save()

	def message(self, *args, **kwargs):
		self.tas = 'crono.tasks.message'
		self.args = args
		self.kwargs = kwargs
		return self.save()

	def email(self, *args, **kwargs):
		self.task = 'crono.tasks.email'
		self.args = args
		self.kwargs = kwargs
		return self.save()

	# Triggers

	def on(self, *args, **kwargs):
		self.trigger = triggers.on(*args, **kwargs)
		return self.save()

	def after(self, *args, **kwargs):
		self.trigger = triggers.after(*args, **kwargs)
		return self.save()

	def every(self, *args, **kwargs):
		self.trigger = triggers.every(*args, **kwargs)
		return self.save()

	def cron(self, *args, **kwargs):
		self.trigger = triggers.cron(*args, **kwargs)
		return self.save()
