import scheduler

from postmarker.core import PostmarkClient


postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))


@scheduler.queue.task
def log(message=None):
	print(message)


@scheduler.queue.task
def email(to=None, body=None):
	print(to, message)
	postmark.emails.send(From='georges@gduverger.com', To=to, Subject='Test', TextBody=body)
