import falcon

from crono import resources
from apscheduler.schedulers.background import BackgroundScheduler

api = falcon.API()
scheduler = BackgroundScheduler()

api.add_route('/', resources.Doc())
api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
