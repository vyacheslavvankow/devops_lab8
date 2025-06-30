import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    return cache.incr('hits')

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

import redis
from flask import Flask, make_response
import socket

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count() -> int:
    return int(cache.get('hits') or 0)

def incr_hit_count() -> int:
    return cache.incr('hits')

@app.route('/metrics')
def metrics():
    metrics = f'''
view_count{{service="Flask-Redis-App"}} {get_hit_count()}
'''
    response = make_response(metrics, 200)
    response.mimetype = "text/plain"
    return response

@app.route('/')
def hello():
    incr_hit_count()
    count = get_hit_count()
    return 'Hello World! I have been seen {} times. My name is: {}\n'.format(count, socket.gethostname())
