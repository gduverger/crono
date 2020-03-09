import os
import uuid
import json
import pytz
import celery
import secrets
import redbeat
import datetime

from crono import queue, triggers


class Job:

	def __init__(self, trigger=None, task=None):
		self.trigger = trigger
		self.task = task

	def save(self):
		if self.task and self.trigger:
			# entry = redbeat.schedulers.RedBeatSchedulerEntry(name=job.key, task=self.task, schedule=self.trigger, args=(job.key,), kwargs=params, app=queue.queue)
			# entry.save()
			pass

		return self

	# def delete(self):
	# 	entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key('redbeat:{}'.format(self.key), app=queue.queue)
	# 	entry.delete()
	# 	return entry

	# Triggers

	def on(self, datetime):
		self.trigger = triggers.datetime(datetime)
		return self.save()

	def in_(self, **kwargs):
		self.trigger = triggers.timer(**kwargs)
		return self.save()

	def every(self, **kwargs):
		self.trigger = triggers.interval(**kwargs)
		return self.save()

	def at(self, string):
		self.trigger = triggers.crontab(string)
		return self.save()

	# Tasks

	def log(self, string):
		self.task = 'crono.tasks.log'
		return self.save()

	def request(self):
		self.task = 'crono.tasks.request'
		return self.save()

	def message(self, text):
		self.tas = 'crono.tasks.message'
		return self.save()

	def email(self):
		self.task = 'crono.tasks.email'
		return self.save()

	def run(self):
		self.task = 'crono.tasks.run'
		return self.save()
