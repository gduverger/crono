# 🔮 Crono

Crono is a **_programmatic_ time-based job scheduler** that gives your application a sense of timing.

```python
import crono
crono.request('POST', 'https://your.app/').after(hours=42)
```

[Read more](https://twitter.com/gduverger/status/1236054680133922816)

## Install

Install package:
```python
pip install crono
```

Run the servers:
```bash
redis-server &
celery worker --app=crono.queue:queue --hostname=worker1@%h
celery beat --app=crono.queue:queue
```

## Usage

### Triggers

A trigger defines when a job will be executed. There are 4 types of triggers: `after`, `on`, `every`, and `cron`. 

**after**

`after` specifies a countdown until the execution of a task. It will only occur once. It takes at least 1 keyword argument: hours, minutes, and/or seconds, of type <int>. Those keywords arguments are cumulative (same for the `every` trigger). For example, `hours=1, minutes=30` equals `minutes=90`.

```python
crono.after(minutes=30).…
```

**on**

`on` specifies the execution of a task at a specific date and time. It will only occur once. It takes 1 positional argument of type `<datetime.datetime>`.

```python
import datetime
date = datetime.datetime(2019, 7, 4)
crono.on(date).…
```

**every**

`every` specifies a frequency at which to execute a task. It will occur multiple times. It takes at least 1 keyword argument: hours, minutes, and/or seconds, of type <int>. Those keywords arguments are cumulative (similarly to the `after` trigger). For example, `hours=1, minutes=30` equals `minutes=90`.

```python
crono.every(hours=1, minutes=30).…
```

**cron**

`cron` uses an expression to specify the execution time. It will occur mutiple times. It takes exactly 1 positional argument of type `<str>`.

```python
crono.cron('0 6 * * 2').…
```

### Tasks

A task defines what a job will do. There are 4 types of tasks: `log`, `request`, `message`, and `email`.

**log**

`log` uses the standard [logging](https://docs.python.org/3.8/library/logging.html) Python library.

```python
crono.log('DEBUG', '{text}', *args, **kwargs)
```

**request**

`request` sends an HTTP request. It is powered by the [Requests](http://docs.python-requests.org/en/master/) library.

```python
crono.request('POST', '{url}', **kwargs).…
```

**message**

`message` sends an SMS. It is powered by [Twilio](https://www.twilio.com/). To use it, you will have to specify `twilio_account_sid` and `twilio_auth_id`.

_Not implemented, yet._

**email**

`email` sends an email. It is powered by [Postmark](https://postmarkapp.com/). To use it, you will have to specify `postmark_api_key` and `postmark_sender`.

_Not implemented, yet._

### Examples

```python
import crono

# Timer
crono.request('POST', '{url}').after(minutes=1)

# Datetime
crono.log('DEBUG', '{text}').on(<datetime>)

# Interval
crono.email(…).every(hours=1) # `email` task not implemented (yet)

# Cron
crono.message(…).cron('0 6 * * 2') # `message` task not implemented (yet)
```

## Configuration

Crono comes with sensible default values that you can override:
```	
# Required
CELERY_BROKER

# Optional
CELERY_RESULT_BACKEND
REDIS_MAX_CONNECTIONS (default: 20)	
CELERY_BROKER_POOL_LIMIT (default: 0)
CELERY_TASK_IGNORE_RESULT (default: True)
CELERY_BEAT_MAX_LOOP_INTERVAL (default: 300)
CELERY_WORKER_MAX_TASKS_PER_CHILD (default: 100)
```	

## Test

```
python -m pytest
```

## Development

Packaging

```console
# Generating distribution archives
$ python setup.py sdist bdist_wheel

# Uploading the distribution archives
$ twine upload --skip-existing dist/*
```
