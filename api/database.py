import os
import json
import secrets

from airtable import airtable


db = airtable.Airtable(os.getenv('AIRTABLE_BASE_ID'), os.getenv('AIRTABLE_API_KEY'))


class User:


	table_name = 'Users'


	def __init__(self, record):
		self.id = record['id']
		self.created_time = record['createdTime']
		self.email = record['fields']['Email']
		self.token = record['fields']['Token']
		self.active = record['fields']['Active']
		self.balance = record['fields']['Balance']
		self.job_ids = record['fields']['Jobs']


	@classmethod
	def get_user(cls, token):
		records = db.get(cls.table_name, filter_by_formula="{{token}}='{}'".format(token))['records']
		return cls(records[0]) if len(records) else None


	def get_jobs(self) -> list:
		return [Job.get_job(self, job_id) for job_id in self.job_ids]


class Job:


	table_name = 'Jobs'


	def __init__(self, user, record):
		# self.user = user
		self.id = record['id']
		self.created_time = record['createdTime']
		self.uuid = record['fields']['uuid']


	@classmethod
	def get_job(cls, user, id_):
		record = db.get(cls.table_name, record_id=id_)
		return cls(user, record) if record else None
