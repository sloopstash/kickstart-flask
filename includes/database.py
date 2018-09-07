# import community modules.
import json
from redis import Redis,ConnectionPool

# import custom modules.
from config import redis_conf

# redis connector.
class redis(object):

  # list of instances created by this class.
  _instances = dict()
 
  # constructor.
  def __new__(self):
    if 'instance' in redis._instances:
      return redis._instances['instance']
    else:
      self.conf = redis_conf
      self.engine = Redis(connection_pool=ConnectionPool(
        host=self.conf['host'],
        port=self.conf['port'],
        max_connections=self.conf['max_connections'],
        db=0
      ))
      return super(redis,self).__new__(self)

  # initializer.
  def __init__(self):
    redis._instances['instance'] = self


redis = redis()