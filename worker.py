import os

import redis
from rq import Worker, Queue, Connection

try:
    listen = ['default']
    redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    conn = redis.from_url(redis_url)
except:
    pass

if __name__ == '__main__':
    try:
        with Connection(conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
    except:
        pass    