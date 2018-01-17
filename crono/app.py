import falcon

from crono import resources

# from apscheduler.schedulers.background import BackgroundScheduler

api = falcon.API()
# scheduler = BackgroundScheduler()

api.add_route('/test', resources.Test())
api.add_route('/jobs', resources.Jobs())
api.add_route('/jobs/{job_id:int}', resources.Job())

# scheduler.start()
