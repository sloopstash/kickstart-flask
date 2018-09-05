# import community modules.
import json

# account controller.
class account(object):

  # initializer.
  def __init__(self,redis):
    self.redis = redis

  # create account.
  def create(self,params):
    return "create account."

  # update account.
  def update(self,id):
    return "update account."

  # delete account.
  def delete(self,id):
    return "delete account."

  # view account.
  def view(self,id):
    return "view account."
