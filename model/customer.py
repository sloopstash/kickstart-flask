##
# -*- coding: utf-8 -*-
##
##
# Customer model.
##

# Import community modules.
import json

# Import custom modules.
from database import redis


# Customer main model.
class customer(object):

  # Initializer.
  def __init__(self):
    self.redis = redis

  # Create customer.
  def create(self, data, user_id):
    try:
      customer_id = self.redis.engine.incr(
        self.redis.conf['key_prefix']['customer']['counter']
      )
      data['user_id'] = user_id  
      self.redis.engine.hset(
        self.redis.conf['key_prefix']['customer']['main'], customer_id, json.dumps(data)
      )
    except Exception as error:
      return False
    else:
      return True

  # Update customer.
  def update(self, data):
    try:
      customer_id = data['customer_id']
      existing_customer = self.redis.engine.hget(self.redis.conf['key_prefix']['customer']['main'], customer_id)   
      if existing_customer:
        current_data = json.loads(existing_customer)
        current_data.update(data)  
        self.redis.engine.hset(self.redis.conf['key_prefix']['customer']['main'], customer_id, json.dumps(current_data))
        return True
      else:
        print("Customer with ID {} not found!".format(customer_id))
        return False
    except Exception as error:
      print("Error updating customer: {}".format(error))
      return False


  # Get customer.
  def get(self,id):
    data = self.redis.engine.hget(
      self.redis.conf['key_prefix']['customer']['main'],id
    )
    if data:
      item = {
        'id':id
      }
      item.update(json.loads(data))
      return item
    else:
      return

  # Count of customers.
  def count(self):
    count = self.redis.engine.hlen(
      self.redis.conf['key_prefix']['customer']['main']
    )
    return count

  # List customers.
  def list(self,**kwargs):
    offset = kwargs['offset'] if kwargs.has_key('offset') else 0
    limit = kwargs['limit'] if kwargs.has_key('limit') else 5
    data = self.redis.engine.hgetall(
      self.redis.conf['key_prefix']['customer']['main']
    )
    items = []
    for key,value in data.items():
      item = {
        'id':key
      }
      item.update(json.loads(value))
      items.append(item)
    return items
  
  # List for user.
  def list_for_user(self, user_id, **kwargs):
    data = self.redis.engine.hgetall(self.redis.conf['key_prefix']['customer']['main'])
    items = []
    for key, value in data.items():
      customer_data = json.loads(value)
      if 'user_id' in customer_data and customer_data['user_id'] == user_id:
        item = {'id': key}
        item.update(customer_data)
        items.append(item)
    print("Items returned by list_for_user:", items) 
    return items

  # Delete customer.
  def delete(self, customer_id):
    customer_key = self.redis.conf['key_prefix']['customer']['main']
    if self.redis.engine.hexists(customer_key, customer_id):
      self.redis.engine.hdel(customer_key, customer_id)
      return True
    else:
      print("Customer {} does not exist.".format(customer_id))  
      return False
