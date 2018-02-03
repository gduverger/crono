import os
import json
import falcon
import celery
import redbeat
import datetime

from api import main, utils, scheduler, triggers, tasks
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
		# jobs = conn.root.get_jobs()
		# TODO

		# task = tasks.add.delay(2, 2)
		# task = tasks.add.apply_async((2, 2), queue='lopri', countdown=10)
		# sender.add_periodic_task(30.0, test.s('world'), expires=10)

		interval = celery.schedules.schedule(run_every=10) # seconds
		entry = redbeat.schedulers.RedBeatSchedulerEntry(name='add every 10 seconds', task='api.tasks.add', schedule=interval, args=[1, 2], app=scheduler.queue)
		entry.save()

		inspect = scheduler.queue.control.inspect()
		print('inspect={} active={} registered={} scheduled={}'.format(inspect, inspect.active(), inspect.registered(), inspect.scheduled()))

		resp.status = falcon.HTTP_OK
		resp.content_type = falcon.MEDIA_JSON
		resp.body = json.dumps(inspect.scheduled())

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

		# Task
		task_params = req.media.get('task')

		if not task_params:
			raise falcon.HTTPMissingParam('task')

		try:
			task = tasks.Task.init(task_params)

		except tasks.TaskException as e:
			raise falcon.HTTPInvalidParam(param_name='task', msg='')

		# Job
		print('[on_post] task.callable={} task.func={} task.params={} trigger.type={} trigger.params={} name={}'.format(task.callable, task.func, task.params, trigger.type, trigger.params, name))
		# job = conn.root.add_job(task.func, kwargs=task.params, name=name, trigger=trigger.type, **trigger.params)
		# TODO

		resp.body = json.dumps(utils.dict_job(job))
		resp.status = falcon.HTTP_CREATED
		resp.content_type = falcon.MEDIA_JSON

	# def on_delete(self, req, resp):
	# 	resp.content_type = falcon.MEDIA_JSON
	# 	conn.root.remove_all_jobs()
	# 	resp.status = falcon.HTTP_OK


class Job(object):

	def on_get(self, req, resp, job_id):
		# job = conn.root.get_job(job_id)
		# TODO

		if job:
			resp.status = falcon.HTTP_OK
			resp.content_type = falcon.MEDIA_JSON
			resp.body = json.dumps(utils.dict_job(job))

		else:
			raise falcon.HTTPNotFound()

	def on_delete(self, req, resp, job_id):
		resp.content_type = falcon.MEDIA_JSON
		# TODO exception handling
		# conn.root.remove_job(job_id)
		# TODO
		resp.status = falcon.HTTP_OK
		resp.body = json.dumps({
			'job': {
				'id': job_id
			}
		})
