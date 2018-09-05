# import community modules.
import json

# contact controller.
class contact(object):

  # initializer.
  def __init__(self,redis):
    self.redis = redis

  # create contact.
  def create(self,params):
    return "create contact."

  # update contact.
  def update(self,id):
    return "update contact."

  # delete contact.
  def delete(self,id):
    return "delete contact."

  # view contact.
  def view(self,id):
    return "view contact."
