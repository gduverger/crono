import scheduler

from api import app


@scheduler.queue.task
def log(message):
	print(message)


@scheduler.queue.task
def email(to=None, body=None):
	print(to, message)
	app.postmark.emails.send(From='georges@gduverger.com', To=to, Subject='Test', TextBody=body)
