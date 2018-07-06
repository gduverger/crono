import os
import uuid
import json
import celery
import secrets
import redbeat
import datetime

from api import scheduler
from apistar import exceptions
from airtable import airtable


db = airtable.Airtable(os.getenv('AIRTABLE_BASE_ID'), os.getenv('AIRTABLE_API_KEY'))


class Log:


	table_name = 'Logs'


	def __init__(self, job):
		self.job = job


	@classmethod
	def add(cls, job):
		log = cls(job)
		db.create(cls.table_name, {
			'Job': [log.job.record_id]
		})
		return log


class Job:


	table_name = 'Jobs'


	def __init__(self, key=None, is_active=True, record_id=None):
		self.key = key or str(uuid.uuid4())
		self.is_active = is_active
		self.record_id = record_id


	@classmethod
	def get(cls, record_id):
		record = db.get(cls.table_name, record_id=record_id)

		if record:
			fields = record['fields']
			return cls(
				key=fields.get('Key'),
				is_active=fields.get('Active', False),
				record_id=record['id']
			)

		else:
			raise exceptions.NotFound('Job not found')


	@classmethod
	def get_by_key(cls, key):
		records = db.get(cls.table_name, filter_by_formula="{{Key}}='{}'".format(key))['records']
		
		if len(records) <= 0:
			raise exceptions.NotFound('Job not found')

		elif len(records) == 1:
			fields = records[0]['fields']
			return cls(
				key=fields.get('Key'),
				is_active=fields.get('Active', False),
				record_id=records[0]['id']
			)

		else:
			raise exceptions.NotFound('More than 1 job found')



	@classmethod
	def add(cls, user, data):
		"""
		For adding, we start with the database and end with the queue.
		"""
		job = cls()

		db.create(cls.table_name, {
			'User': [user.record_id],
			'Key': job.key,
			'Active': job.is_active
		})

		schedule = None
		if data.trigger['name'] == 'crontab':
			minute, hour, day_of_month, month_of_year, day_of_week = data.trigger['params']['expression'].split(' ')
			schedule = celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=scheduler.queue)

		elif data.trigger['name'] == 'interval':
			# seconds = datetime.timedelta(seconds=data.trigger['params']['seconds'])
			# schedule = celery.schedules.schedule(run_every=seconds, app=scheduler.queue)
			raise exceptions.MethodNotAllowed("Trigger 'interval' not implemented yet")

		elif data.trigger['name'] == 'eta':
			# datetime_ = dateparser.parse(data.trigger['params']['datetime'])
			# schedule = redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=scheduler.queue) # HACK
			raise exceptions.MethodNotAllowed("Trigger 'ETA' not implemented yet")

		elif data.trigger['name'] == 'countdown':
			# seconds = data.trigger['params']['seconds']
			# schedule = redbeat.schedules.rrule('SECONDLY', interval=seconds, count=1, app=scheduler.queue)
			raise exceptions.MethodNotAllowed("Trigger 'countdown' not implemented yet")

		params = data.task['params']
		task = 'api.tasks.{}'.format(data.task['name'])
		entry = redbeat.schedulers.RedBeatSchedulerEntry(name=job.key, task=task, schedule=schedule, args=(job.key,), kwargs=params, app=scheduler.queue)
		entry.save()

		return job


	def add_log(self):
		return Log.add(self)


	def remove(self):
		"""
		For removing, we start with the queue and end with the database.
		"""

		try:
			entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(self.key, app=scheduler.queue)
			entry.delete()
			self.is_active = False
			db.update(self.table_name, self.record_id, {'Active': self.is_active})

		except KeyError:
			db.delete(self.table_name, self.record_id)

		return self


	def to_dict(self) -> dict:
		return {
			'key': self.key,
		}


class User:


	table_name = 'Users'


	def __init__(self, email, token=None, is_active=True, jobs=None, record_id=None):
		self.email = email
		self.token = token or secrets.token_hex()
		self.is_active = is_active
		self.jobs = jobs
		self.record_id = record_id


	@classmethod
	def get(cls, token):
		records = db.get(cls.table_name, filter_by_formula="{{token}}='{}'".format(token))['records']

		if len(records) <= 0:
			raise exceptions.NotFound('User not found')

		elif len(records) == 1:
			fields = records[0]['fields']
			return cls(
				fields['Email'],
				token=fields.get('Token'),
				is_active=fields.get('Active', False),
				jobs=[Job.get(record_id) for record_id in fields.get('Jobs', [])],
				record_id=records[0]['id']
			)

		else:
			raise exceptions.NotFound('More than 1 user found')


	@classmethod
	def add(cls, email):
		user = cls(email)
		db.create(cls.table_name, {
			'Email': user.email,
			'Token': user.token,
			'Active': user.is_active,
		})
		return user


	def get_jobs(self) -> list:
		return [job for job in self.jobs if job.is_active]


	def get_job(self, key) -> Job:

		for job in self.get_jobs():

			if job.key == key:
				return job

		raise exceptions.NotFound('Job not found')


	def add_job(self, data) -> Job:
		job = Job.add(self, data)
		self.jobs.append(job)
		return job


	def remove_job(self, key) -> Job:
		job = self.get_job(key)
		job.remove()
		return job


	def to_dict(self) -> dict:
		return {
			'email': self.email,
			'token': self.token,
		}
