import os
import uuid
import redbeat
import logging

from crono import queue, triggers


class Job:

	def __init__(self, trigger=None, task=None, args=None, kwargs=None):
		self.trigger = trigger
		self.task = task
		self.args = args
		self.kwargs = kwargs

	def save(self):

		if self.task and self.trigger != None:
			name = str(uuid.uuid4())
			entry = redbeat.schedulers.RedBeatSchedulerEntry(name=name, task=self.task, schedule=self.trigger, args=self.args, kwargs=self.kwargs, app=queue.queue)
			logging.debug(entry)
			entry.save()

		return self

	# def delete(self):
	# 	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key('redbeat:{}'.format(self.key), app=queue.queue)
	# 	entry.delete()
	# 	return entry

	# Triggers

	def on(self, *args, **kwargs):
		self.trigger = triggers.date(*args, **kwargs)
		return self.save()

	def after(self, *args, **kwargs):
		self.trigger = triggers.timer(*args, **kwargs)
		return self.save()

	def every(self, *args, **kwargs):
		self.trigger = triggers.interval(*args, **kwargs)
		return self.save()

	def at(self, *args, **kwargs):
		# TODO https://en.wikipedia.org/wiki/At_(command)
		raise Exception('not implemented')

	def cron(self, *args, **kwargs):
		self.trigger = triggers.cron(*args, **kwargs)
		return self.save()

	def when(self, *args, **kwargs):
		self.trigger = triggers.solar(*args, **kwargs)
		return self.save()

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
