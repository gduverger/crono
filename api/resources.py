import os
import json
import falcon
import datetime

from api import main, utils
from apscheduler.jobstores.base import JobLookupError


class Jobs(object):

	def on_get(self, req, resp):
		jobs = main.scheduler.get_jobs(jobstore='redis')
		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps([utils.jsonify_job(job) for job in jobs])

	def on_post(self, req, resp):
		command = req.params.get('command')
		trigger = req.params.get('trigger')
		name = req.params.get('name')
		
		seconds = req.params.get('seconds')
		text = req.params.get('text')

		if not command:
			raise falcon.HTTPMissingParam('command')

		elif command not in ['log']: # 'get', 'post', 'email', 'text', 'call'
			raise falcon.HTTPInvalidParam('It should be one of the following: log.', 'command')

		if not trigger:
			raise falcon.HTTPMissingParam('trigger')

		elif trigger not in ['interval']: # 'date', 'cron'
			raise falcon.HTTPInvalidParam('It should be one of the following: interval.', 'trigger')

		job = main.scheduler.add_job('api.commands:{}'.format(command), args=(text,), trigger=trigger, name=name, seconds=int(seconds), jobstore='redis')

		resp.status = falcon.HTTP_CREATED
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps(utils.jsonify_job(job))

	def on_delete(self, req, resp):
		resp.content_type = falcon.MEDIA_JSON
		main.scheduler.remove_all_jobs(jobstore='redis')
		resp.status = falcon.HTTP_OK


class Job(object):

	def on_get(self, req, resp, job_id):
		job = main.scheduler.get_job(job_id, jobstore='redis')

		if job:
			resp.status = falcon.HTTP_OK
			resp.content_type = falcon.MEDIA_JSON
			resp.body = json.dumps(utils.jsonify_job(job))

		else:
			raise falcon.HTTPNotFound()

	def on_delete(self, req, resp, job_id):
		resp.content_type = falcon.MEDIA_JSON

		try:
			main.scheduler.remove_job(job_id, jobstore='redis')
			resp.status = falcon.HTTP_OK
			resp.body = json.dumps({
				'job': {
					'id': job_id
				}
			})

		except JobLookupError as e:
			raise falcon.HTTPNotFound()
