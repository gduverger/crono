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

```python
import crono

# Timer
crono.request('POST', '{url}').after(minutes=1)

# Datetime
crono.log('{text}').on(<datetime>)

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
