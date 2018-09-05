# import community modules.
import json

# lead controller.
class lead(object):

  # initializer.
  def __init__(self,redis):
    self.redis = redis

  # create lead.
  def create(self,params):
    return "create lead."

  # update lead.
  def update(self,id):
    return "update lead."

  # delete lead.
  def delete(self,id):
    return "delete lead."

  # view lead.
  def view(self,id):
    return "view lead."
