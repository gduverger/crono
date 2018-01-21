import os
import json
import falcon
import datetime

from api import main, utils, triggers, commands
from apscheduler.jobstores.base import JobLookupError


class Index(object):

	auth = {'exempt_methods': ['GET']}

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_HTML
		with open('{}/static/index.html'.format(main.DIR_PATH), 'r') as file:
			resp.body = file.read()


class Jobs(object):

	def on_get(self, req, resp):
		jobs = main.scheduler.get_jobs(jobstore='redis')
		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps([utils.jsonify_job(job) for job in jobs])

	def on_post(self, req, resp):
		# Name (optional)
		name = req.params.get('name', 'Job')

		# Trigger
		trigger_params = req.media.get('trigger')

		if not trigger_params:
			raise falcon.HTTPMissingParam('trigger')

		try:
			trigger = triggers.Trigger.init(trigger_params)

		except triggers.TriggerException as e:
			raise falcon.HTTPInvalidParam(param_name='trigger', msg='')			

		# Command
		command_params = req.media.get('command')

		if not command_params:
			raise falcon.HTTPMissingParam('command')

		try:
			command = commands.Command.init(command_params)

		except commands.CommandException as e:
			raise falcon.HTTPInvalidParam(param_name='command', msg='')

		# Job
		job = main.scheduler.add_job(command.callable, kwargs=command.params, trigger=trigger.type, **trigger.params, name=name, jobstore='redis')

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
