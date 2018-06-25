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
				key=fields['Key'],
				is_active=fields.get('Active', False),
				record_id=record['id']
			)

		else:
			raise exceptions.NotFound('Job not found')


	@classmethod
	def add(cls, user, data):
		"""
		schedule = None

		if job.trigger['name'] == 'interval':
			seconds = datetime.timedelta(seconds=job.trigger['params']['seconds'])
			schedule = celery.schedules.schedule(run_every=seconds, app=scheduler.queue)

		elif job.trigger['name'] == 'crontab':
			minute, hour, day_of_month, month_of_year, day_of_week = job.trigger['params']['expression'].split(' ')
			schedule = celery.schedules.crontab(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year, app=scheduler.queue)

		elif job.trigger['name'] == 'eta':
			# datetime_ = dateparser.parse(job.trigger['params']['datetime'])
			# schedule = redbeat.schedules.rrule('SECONDLY', dtstart=datetime_, count=1, app=scheduler.queue) # HACK
			raise Exception('Not implemented yet')

		elif job.trigger['name'] == 'countdown':
			# seconds = job.trigger['params']['seconds']
			# schedule = redbeat.schedules.rrule('SECONDLY', interval=seconds, count=1, app=scheduler.queue)
			raise Exception('Not implemented yet')

		params = job.task['params']
		task = 'api.tasks.{}'.format(job.task['name'])
		entry = redbeat.schedulers.RedBeatSchedulerEntry(name=datetime.datetime.now().isoformat(), task=task, schedule=schedule, kwargs=params, app=scheduler.queue)
		entry.save()
		"""

		job = cls()

		db.create(cls.table_name, {
			'User': [user.record_id],
			'Key': job.key,
			'Active': job.is_active
		})

		return job


	def remove(self):
		"""
		entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(self.key, app=scheduler.queue)
		entry.delete()
		"""
		self.is_active = False
		db.update(self.table_name, self.record_id, {'Active': self.is_active})
		return self


	def to_dict(self) -> dict:
		return {
			'key': self.key,
		}


class User:


	table_name = 'Users'


	def __init__(self, email, token=None, balance=1, is_active=True, jobs=None, record_id=None):
		self.email = email
		self.token = token or secrets.token_hex()
		self.balance = balance
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
				balance=fields.get('Balance'),
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
			'Balance': user.balance
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
			'balance': self.balance
		}
