import falcon

from resources import jobs

app = falcon.API()
jobs = jobs.JobsResource()
app.add_route('/jobs', jobs)
