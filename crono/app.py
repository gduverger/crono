import falcon

from crono import jobs

# from apscheduler.schedulers.background import BackgroundScheduler

api = falcon.API()
# scheduler = BackgroundScheduler()

jobs = jobs.JobsResource()
api.add_route('/jobs', jobs)

# scheduler.start()
