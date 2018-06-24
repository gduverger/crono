import os
import uuid
import json
import celery
import secrets
import redbeat
import datetime

from api import scheduler
from airtable import airtable


db = airtable.Airtable(os.getenv('AIRTABLE_BASE_ID'), os.getenv('AIRTABLE_API_KEY'))


class Job:


	table_name = 'Jobs'


	def __init__(self, uuid=None, key=None, active=True, record_id=None):
		self.uuid = uuid or uuid.uuid4()
		self.key = key
		self.active = active
		self.record_id = record_id


	@classmethod
	def get(cls, record_id):
		record = db.get(cls.table_name, record_id=record_id)

		if record:
			fields = record['fields']
			return cls(
				uuid=fields['uuid'],
				key=fields['Key'],
				active=fields.get('Active', False),
				record_id=record['id']
			)

		else:
			raise Exception('Job not found')


	@classmethod
	def add(cls, job):
		# TODO schedule
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

		job = cls(key=entry.key)

		# TODO persist

		return job


	def remove(self):
		entry = redbeat.schedulers.RedBeatSchedulerEntry.from_key(self.key, app=scheduler.queue)
		entry.delete()
		self.active = False
		db.update(self.table_name, self.record_id, {'Active': self.active})
		return self


	def to_dict(self) -> dict:
		return {
			'uuid': self.uuid,
		}


class User:


	table_name = 'Users'


	def __init__(self, email, token=None, balance=1, is_active=True, jobs=None):
		self.email = email
		self.token = token or secrets.token_hex()
		self.balance = balance
		self.is_active = is_active
		self.jobs = jobs


	@classmethod
	def get(cls, token):
		records = db.get(cls.table_name, filter_by_formula="{{token}}='{}'".format(token))['records']

		if len(records) <= 0:
			raise Exception('User not found')

		elif len(records) == 1:
			fields = records[0]['fields']
			return cls(
				fields['Email'],
				token=fields.get('Token'),
				balance=fields.get('Balance'),
				is_active=fields.get('Active', False),
				jobs=[Job.get(record_id) for record_id in fields.get('Jobs', [])]
			)

		else:
			raise Exception('More than 1 user found')


	@classmethod
	def add(cls, email):
		user = cls(email)
		fields = {
			'Email': user.email,
			'Token': user.token,
			'Active': user.is_active,
			'Balance': user.balance
		}
		db.create(cls.table_name, fields)
		return user


	def get_jobs(self) -> list:
		return [j for j in self.jobs if j.active]


	def get_job(self, uuid) -> Job:

		for job in self.get_jobs():

			if job.uuid == uuid:
				return job

		raise Exception('Job not found')


	def add_job(self, data) -> Job:
		job = Job.add(data)
		self.jobs.append(job)
		return job


	def remove_job(self, uuid) -> Job:
		job = self.get_job(uuid)
		job.remove()
		return job


	def to_dict(self) -> dict:
		return {
			'email': self.email,
			'token': self.token,
			'balance': self.balance
		}
