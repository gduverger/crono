import falcon

from crono import resources

# from apscheduler.schedulers.background import BackgroundScheduler

api = falcon.API()
# scheduler = BackgroundScheduler()

jobs = resources.Jobs()
api.add_route('/jobs', jobs)

tests = resources.Tests()
api.add_route('/tests', tests)

# scheduler.start()
