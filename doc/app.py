from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'crono'

if __name__ == '__main__':
	app.run('127.0.0.1', 8000, debug=True)
