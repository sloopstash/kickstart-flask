##
# -*- coding: utf-8 -*-
##
##
# Contact controller.
##

# Import community modules.
import math
import logging
from decimal import Decimal
from flask import render_template, jsonify, redirect, request

# Import custom modules.
from controller import root_web_controller
from model.customer import customer
from model.contact import contact

# Contact web controller.
class contact_web_controller(root_web_controller):

  # HTTP GET method processor.
  def get(self,*args,**kwargs):
    if self.request.path == '/contacts':
      if self.request.args.get('count'):
        contacts = contact().count()
        if contacts>0:
          limit = Decimal(5.0)
          pages = math.ceil(contacts/limit)
          return jsonify({'status': 'success', 'result': {'count': contacts, 'pages': int(pages)}})
        else:
          return jsonify({'status': 'failure', 'message': 'Not available.'})
      else:
        limit = 5
        offset = (int(self.request.args.get('page'))*limit)-limit if self.request.args.get('page') else 0
        contacts = contact().list(offset=offset,limit=limit)
        return jsonify({'status':'success','result': {'items': contacts}})
    elif self.request.path=='/customer/'+args[0]+'/dashboard':
      customer_id = args[0]
      self.var['customer'] = customer().get(customer_id)
      self.var['contacts'] = contact().list_for_customer(customer_id)
      print("Fetched contacts for customer {}: {}".format(customer_id, self.var['contacts']))  # Debugging line
      return render_template('customer/dashboard.html', var=self.var)
    elif self.request.path=='/customer/'+args[0]+'/contact/create':
      customer_id = args[0]
      self.var['customer'] = customer().get(customer_id)
      self.var['contacts'] = contact().list_for_customer(customer_id) 
      print self.var['customer']
      return render_template('contact/create.html',var=self.var)
    elif len(args) < 2:
      self.var['error_message'] = "Missing customer or contact ID."
      return render_template('error.html', var=self.var)
    elif self.request.path=='/customer/'+args[0]+'/contact/'+args[1]+'/update':
      contact_id = args[1]
      customer_id = args[0]  
      if 'contact' in self.var: 
        print(self.var['contact']) 
      else:
        print("Contact data not found!")
      self.var['contact'] = contact().get(customer_id, contact_id) 
      self.var['customer'] = customer().get(customer_id)
      return render_template('contact/update.html', var=self.var) 
    elif len(args) < 2:
      self.var['error_message'] = "Missing customer or contact ID."
      return render_template('error.html', var=self.var) 
    elif self.request.path == '/customer/'+args[0] +'/contact/'+args[1]+'/delete':
      customer_id = args[0]
      contact_id = args[1]
      if contact().delete(contact_id):
        return redirect('/customer/'+args[0]+'/dashboard')
    else:
      self.var['error_message'] = "There was an issue deleting the contact."
      return render_template('error.html', var=self.var)

  # HTTP POST method processor.
  def post(self, *args, **kwargs):
    if self.request.path=='/customer/'+args[0]+'/contact/create':
      data = {
        'firstname': self.request.form.get('firstname'),
        'lastname': self.request.form.get('lastname'),
        'email': self.request.form.get('email'),
        'phonenumber': self.request.form.get('phonenumber'),
        'description': self.request.form.get('description'),
      }
      if contact().create(args[0], data) is True: 
        return redirect('/customer/'+ args[0] +'/dashboard')
      else:
        self.var['error_message'] = "There was an issue creating the contact."
        return render_template('error.html', var=self.var)
    elif self.request.path =='/customer/'+args[0]+'/contact/'+args[1]+'/update':
      data = {
        'contact_id': args[1],
        'firstname': self.request.form.get('firstname'),
        'lastname': self.request.form.get('lastname'),
        'email': self.request.form.get('email'),
        'phonenumber': self.request.form.get('phonenumber'),
        'description': self.request.form.get('description'),
        'customer_id': args[0] 
      }
      data['contact_id'] = args[1]
      if contact().update(data) is True:
        self.var['contact'] = contact().get(args[0], args[1]) 
        self.var['contacts'] = contact().list_for_customer(args[0])
        self.var['customer'] = customer().get(args[0]) 
        return redirect('/customer/'+args[0]+'/dashboard')
      else:
        return render_template('error.html', var=self.var)

    elif self.request.path =='/customer/'+args[0]+'/contact/'+args[1]+'/delete':
      customer_id = args[0]
      contact_id = args[1]
      if contact().delete(customer_id, contact_id):
        return redirect('/customer/'+args[0]+'/dashboard')
      else:
        self.var['error_message'] = "There was an issue deleting the contact."
        return render_template('error.html', var=self.var)
    else:
        return render_template('error.html', var=self.var)