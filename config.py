# import community modules.
import json

# get redis configuration.
def redis_conf():
  file = open('config/redis.conf','r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf

redis_conf = redis_conf()