import datetime

from api import main


def log(text):
	print(text)
	main.queue.enqueue(print, args=(text,))

def get(url):
	pass

# def post(url):
# 	pass

def email(subject, body):
	pass

def text(number, text):
	pass

# def call(number, text):
# 	pass
