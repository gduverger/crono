# 🔮 Crono

Crono is a programmatic time-based job scheduler so you can give your application a sense of timing.

[Read more](https://twitter.com/gduverger/status/1236054680133922816)

## Install

Install the library:
```python
pip install crono
```

Run the servers:
```bash
redis-server &
celery worker --app=crono.queue:queue --hostname=worker1@%h --loglevel=DEBUG
celery beat --app=crono.queue:queue --loglevel=DEBUG
```

Stop the (redis) server and reset it, if necessary:
```
redis-cli flushall
redis-cli shutdown
```

## Usage

### Triggers

A trigger defines when a job will be executed. There are 5 types of triggers: `after`, `on`, `every`, `cron`, and `at`\*. 

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

There are 4 tasks you can perform with Crono: `log`, `request`, `message`\*, and `email`\*.  
\* not implemented (yet)

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
REDIS_MAX_CONNECTIONS (default: 20)	
CELERY_BROKER
CELERY_RESULT_BACKEND
CELERY_BROKER_POOL_LIMIT (default: 0)
CELERY_TASK_IGNORE_RESULT (default: True)
CELERY_BEAT_MAX_LOOP_INTERVAL (default: 300)
CELERY_WORKER_MAX_TASKS_PER_CHILD (default: 100)
```	

## Test

```
python -m pytest
celery flower -app=crono.queue:queue --address=127.0.0.1 --port=5555 --broker=redis://localhost:6379/0
```
