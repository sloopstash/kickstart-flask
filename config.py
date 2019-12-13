# import community modules.
import json

# get app configuration.
def app_conf():
  file = open('config/app.conf','r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf

# get redis configuration.
def redis_conf():
  file = open('config/redis.conf','r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf

app_conf = app_conf()
redis_conf = redis_conf()
