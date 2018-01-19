import datetime

from api import main


def log(text):
	print(text)
	main.queue.enqueue(print, args=(text,))

def get(url):
	pass

# def post(url):
# 	pass

def email(subject='Subject', body='Body'):
	main.postmark.emails.send(From='log@airquote.co', To='georges.duverger@gmail.com', Subject=subject, TextBody=body)


def text(number, text):
	pass

# def call(number, text):
# 	pass
