import os
import json
import rpyc
import falcon
import datetime

from api import main, utils, triggers, commands
from apscheduler.jobstores.base import JobLookupError


conn = rpyc.connect(os.getenv('RPYC_HOSTNAME', 'localhost'), int(os.getenv('RPYC_PORT', 12345)), config={'allow_all_attrs': True})


class Index(object):

	auth = {'exempt_methods': ['GET']}

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_HTML
		with open('{}/static/index.html'.format(main.DIR_PATH), 'r') as file:
			resp.body = file.read()


class Jobs(object):

	def on_get(self, req, resp):
		jobs = conn.root.get_jobs()
		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps([utils.dict_job(job) for job in jobs])

	def on_post(self, req, resp):
		# Name (optional)
		name = req.media.get('name', 'Job')

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
		print('[on_post] command.callable={} command.func={} command.params={} trigger.type={} trigger.params={} name={}'.format(command.callable, command.func, command.params, trigger.type, trigger.params, name))
		job = conn.root.add_job(command.func, kwargs=command.params, name=name, trigger=trigger.type, **trigger.params)

		resp.body = json.dumps(utils.dict_job(job))
		resp.status = falcon.HTTP_CREATED
		resp.content_type = falcon.MEDIA_JSON

	# def on_delete(self, req, resp):
	# 	resp.content_type = falcon.MEDIA_JSON
	# 	conn.root.remove_all_jobs()
	# 	resp.status = falcon.HTTP_OK


class Job(object):

	def on_get(self, req, resp, job_id):
		job = conn.root.get_job(job_id)

		if job:
			resp.status = falcon.HTTP_OK
			resp.content_type = falcon.MEDIA_JSON
			resp.body = json.dumps(utils.dict_job(job))

		else:
			raise falcon.HTTPNotFound()

	def on_delete(self, req, resp, job_id):
		resp.content_type = falcon.MEDIA_JSON
		# TODO exception handling
		conn.root.remove_job(job_id)
		resp.status = falcon.HTTP_OK
		resp.body = json.dumps({
			'job': {
				'id': job_id
			}
		})
