# Import community modules.
import os
import json

# Get App configuration.
def app_conf():
  file = open('config/app.conf','r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf

# Get Redis configuration.
def redis_conf():
  file = open('config/redis.conf','r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  if 'STATIC_ENDPOINT' in os.environ:
    conf['cdn']['static']['endpoint'] = os.environ['STATIC_ENDPOINT']
  return conf

app_conf = app_conf()
redis_conf = redis_conf()
