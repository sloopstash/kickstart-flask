##
# -*- coding: utf-8 -*-
##
##
# Customer model.
##

# Import community modules.
import json
import logging

# Import custom modules.
from database import redis


# Customer main model.
class contact(object):

  # Initializer.
  def __init__(self):
    self.redis = redis

  def create(self, customer_id, data):
    try:
      contact_id = self.redis.engine.incr(
        self.redis.conf['key_prefix']['contact']['counter']
      )
      contact_key = "customer:{}:contact:{}".format(customer_id, contact_id)
      data['id'] = contact_id

      for key, value in data.items():
        self.redis.engine.hset(contact_key, key, value)

    except Exception as error:
      print("Error creating contact: {}".format(error))  
      return False
    else:
      print("Contact created successfully with ID {}".format(contact_id))  
      return True
 

  # Update contact.
  def update(self, data):
    try:
      contact_id = data['contact_id']
      customer_id = data['customer_id']
      contact_key = "customer:{}:contact:{}".format(customer_id, contact_id)
      contact_data = self.redis.engine.hgetall(contact_key)
      if not contact_data:
        return False
      for field, value in data.items():
        self.redis.engine.hset(contact_key, field, value)
    except Exception as error:
      return False
    else:
      return True

  # Get contact.
  def get(self, customer_id, contact_id):
    try:
      key = "customer:{}:contact:{}".format(customer_id, contact_id)
      data = self.redis.engine.hgetall(key)
      if data:
        item = {
        'id': contact_id
        }
        item.update(data)
        return item
      else:
        return None
    except redis.ConnectionError as e:
      return None
    except redis.RedisError as e:
      return None
    except Exception as e:
      return None

  # Count of contact.
  def count(self):
    count = self.redis.engine.hlen(
      self.redis.conf['key_prefix']['contact']['main']
    )
    return count

  # List customers.
  def list(self,**kwargs):
    offset = kwargs['offset'] if kwargs.has_key('offset') else 0
    limit = kwargs['limit'] if kwargs.has_key('limit') else 5
    data = self.redis.engine.hgetall(
      self.redis.conf['key_prefix']['contact']['main']
    )
    items = []
    for key,value in data.items():
      item = {
        'id':key
      }
      item.update(json.loads(value))
      items.append(item)
    return items

  # List for customers
  def list_for_customer(self, customer_id):
    try:
      keys = self.redis.engine.keys("customer:{}:contact:*".format(customer_id))
      print "Fetched keys for customer {}: {}".format(customer_id, keys)  
      if not keys:
        return []
      items = []
      for key in keys:
        contact_data = self.redis.engine.hgetall(key)
        contact_id = key.split(":")[-1]  
        contact_data['id'] = contact_id
        items.append(contact_data)
      print "Returning contacts for customer {}: {}".format(customer_id, items)
      return items
    except Exception as e:
      print("Error fetching contacts:", e)  
      return [] 

  # Delete contact.
  def delete(self, customer_id, contact_id):
    try:
      contact_key = "customer:{}:contact:{}".format(customer_id, contact_id)
      if not self.redis.engine.exists(contact_key):
        return False
      self.redis.engine.delete(contact_key)
      return True
    except Exception as error:
      return False

  