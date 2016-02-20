"""
Monkey patch configuration here...
"""
import redis
import os

CLIENT = redis.StrictRedis.from_url(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))

