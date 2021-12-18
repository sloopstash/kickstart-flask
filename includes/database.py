# Import community modules.
import json
from redis import Redis,ConnectionPool

# Import custom modules.
from config import redis_conf

# Redis connector.
class redis(object):

  # List of instances created by this class.
  _instances = dict()
 
  # Constructor.
  def __new__(self):
    if 'instance' in redis._instances:
      return redis._instances['instance']
    else:
      self.conf = redis_conf
      self.engine = Redis(connection_pool=ConnectionPool(
        host=self.conf['host'],
        port=self.conf['port'],
        max_connections=self.conf['max_connections'],
        db=0,
        decode_responses=True
      ))
      return super(redis,self).__new__(self)

  # Initializer.
  def __init__(self):
    redis._instances['instance'] = self


redis = redis()