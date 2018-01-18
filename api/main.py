import falcon

from rq import Queue
from api import worker, resources
from apscheduler.schedulers.background import BackgroundScheduler

api = falcon.API()
scheduler = BackgroundScheduler()
queue = Queue(connection=worker.conn)

api.add_route('/', resources.Doc())
api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id}', resources.Job())

scheduler.start()
