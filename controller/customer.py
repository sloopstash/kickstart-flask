##
# -*- coding: utf-8 -*-
##
##
# Customer controller.
##

# Import community modules.
import math
from decimal import Decimal
from flask import render_template,jsonify,redirect
from flask import session


# Import custom modules.
from controller import root_web_controller
from model.customer import customer
from model.contact import contact  # Add this import

# Customer web controller.
class customer_web_controller(root_web_controller):

  # HTTP GET method processor.
  def get(self,*args,**kwargs):
    user_id = self._get_authenticated_user_id()
    if self.request.path=='/customers':
      if self.request.args.get('count'):
        customers = customer().count()
        if customers>0:
          limit = Decimal(5.0)
          pages = math.ceil(customers/limit)
          return jsonify({'status':'success','result':{'count':customers,'pages':int(pages)}})
        else:
          return jsonify({'status':'failure','message':'Not available.'})
      else:
        limit = 5
        offset = (int(self.request.args.get('page'))*limit)-limit if self.request.args.get('page') else 0
        customers = customer().list_for_user(user_id, offset=offset, limit=limit)  
        return jsonify({'status':'success','result':{'items':customers}})
    elif self.request.path=='/customer/create':
      return render_template('customer/create.html',var=self.var)
    elif self.request.path=='/customer/'+args[0]+'/update':
      customer_id = args[0]
      self.var['customer'] = customer().get(customer_id)
      return render_template('customer/update.html',var=self.var)
    elif self.request.path=='/customer/'+args[0]+'/dashboard':
      customer_id = args[0]
      customer_data = customer().get(customer_id)
      if customer_data and customer_data['user_id'] == user_id:  
        self.var['customer'] = customer_data
        contacts = contact().list_for_customer(customer_id)
        self.var['contacts'] = contacts
        return render_template('customer/dashboard.html',var=self.var)
      else:
         return redirect('/login') 
    else:
      return render_template('error.html',var=self.var)

  # HTTP POST method processor.
  def post(self,*args,**kwargs):
    if self.request.path=='/customer/create':
      data = {
        'name':self.request.form.get('name'),
        'email':self.request.form.get('email'),
        'phone':self.request.form.get('phone'),
        'website':self.request.form.get('website'),
        'description':self.request.form.get('description')
      }
      user_id = self._get_authenticated_user_id()
      # if customer().create(data) is True:
      if customer().create(data, user_id) is True:
        return redirect('/dashboard')
      else:
        return render_template('error.html',var=self.var)
    elif self.request.path=='/customer/'+args[0]+'/update':
      data = {
        'name':self.request.form.get('name'),
        'email':self.request.form.get('email'),
        'phone':self.request.form.get('phone'),
        'website':self.request.form.get('website'),
        'description':self.request.form.get('description')
      }
      data['customer_id'] = args[0]
      if customer().update(data) is True:
        return redirect('/dashboard')
      else:
        return render_template('error.html',var=self.var)
    
    elif self.request.path == '/customer/' + args[0] + '/delete':
      user_id = self._get_authenticated_user_id()
      customer_id = args[0]
      customer_data = customer().get(customer_id)
      if customer_data and customer_data['user_id'] == user_id:
       try:
         if customer().delete(customer_id):
           return jsonify({'status': 'success', 'message': 'Customer deleted successfully.', 'refresh': True})
         else:
           return jsonify({'status': 'failure', 'message': 'Failed to delete customer.'})
       except Exception as e:
          app.logger.error("Error occurred while deleting customer {}: {}".format(customer_id, str(e)))
          return jsonify({'status': 'failure', 'message': "Error occurred while deleting customer: {}".format(str(e))})
      else:
        return jsonify({'status': 'failure', 'message': 'Customer not found or you do not have permission.'})
    else:
      return render_template('error.html',var=self.var)
  
  def _get_authenticated_user_id(self):
    user_id = session.get('user_id')  
    if not user_id:
      return None 
      # raise Exception("User is not authenticated")
    return user_id