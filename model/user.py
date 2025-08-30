# -*- coding: utf-8 -*-
##
##
# User model.
##

# Import community modules.
import json

# Import custom modules.
from database import redis


# User main model.
class user(object):

  # Initializer.
  def __init__(self):
    self.redis = redis

  # Create user.
  def create(self, username, password, email):
    try:
      user_data = {
      'username': username,
      'password': password,  
      'email': email
      }
      user_id = self.redis.engine.incr(self.redis.conf['key_prefix']['user']['counter'])
      self.redis.engine.hset(self.redis.conf['key_prefix']['user']['main'], user_id, json.dumps(user_data))
    except Exception as error:
      return False
    else:
      return user_id

  # Authenticate user.
  def authenticate(self, username, password):
    for user_id in self.redis.engine.hkeys(self.redis.conf['key_prefix']['user']['main']):
      user_data = json.loads(self.redis.engine.hget(self.redis.conf['key_prefix']['user']['main'], user_id))
      if user_data['username'] == username and user_data['password'] == password:
        return {'id': user_id, 'username': username}  
    return None

  # Get user by ID.
  def get(self, user_id):
    user_data = self.redis.engine.hget(self.redis.conf['key_prefix']['user']['main'], user_id)
    if user_data:
      user_info = json.loads(user_data)
      user_info['id'] = user_id
      return user_info
    return None
