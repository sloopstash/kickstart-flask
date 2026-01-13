##
# -*- coding: utf-8 -*-
##
##
# Bootstrap CRM app service.
##

# Import community modules.
import sys

# Append App specific Python paths.
sys.path.append('model')
sys.path.append('controller')
sys.path.append('helper')

# Import community modules.
import argparse
from flask import Flask,request
from elasticapm.contrib.flask import ElasticAPM

# Import custom modules.
from controller.user import user_web_controller
from controller.customer import customer_web_controller
from controller.contact import contact_web_controller


# Health web controller.
def health_web_controller():
  return str('OK')

# View dashboard.
def dashboard():
  if request.method=='GET':
    return user_web_controller(request).get()
  else:
    return None

# Create customer.
def create_customer():
  if request.method=='GET':
    return customer_web_controller(request).get()
  elif request.method=='POST':
    return customer_web_controller(request).post()
  else:
    return None

# Update customer.
def update_customer(arg_0):
  if request.method=='GET':
    return customer_web_controller(request).get(str(arg_0))
  elif request.method=='POST':
    return customer_web_controller(request).post(str(arg_0))
  else:
    return None

# List customers.
def list_customers():
  if request.method=='GET':
    return customer_web_controller(request).get()
  else:
    return None

# Create contact.
def create_contact(arg_0):
  if request.method=='GET':
    return contact_web_controller(request).get(str(arg_0))
  elif request.method=='POST':
    return contact_web_controller(request).post(str(arg_0))
  else:
    return None

# Update contact.
def update_contact(arg_0,arg_1):
  if request.method=='GET':
    return contact_web_controller(request).get(str(arg_0),str(arg_1))
  elif request.method=='POST':
    return contact_web_controller(request).post(str(arg_0),str(arg_1))
  else:
    return None

# List contacts.
def list_contacts():
  if request.method=='GET':
    return contact_web_controller(request).get()
  else:
    return None


# Initialize Flask app.
app = Flask('SloopStash CRM app',template_folder='view')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME':'SloopStash CRM app',
  'SECRET_TOKEN':'',
  'SERVER_URL':'http://apm:8200',
  'DEBUG':True
}
apm = ElasticAPM(app,logging=True)

# App routes.
app.add_url_rule('/health',view_func=health_web_controller)
app.add_url_rule('/dashboard',view_func=dashboard)
app.add_url_rule('/customer/create',view_func=create_customer,methods=['GET','POST'])
app.add_url_rule('/customer/<int:arg_0>/update',view_func=update_customer,methods=['GET','POST'])
app.add_url_rule('/customers',view_func=list_customers)
app.add_url_rule('/customer/<int:arg_0>/contact/create',view_func=create_contact,methods=['GET','POST'])
app.add_url_rule('/customer/<int:arg_0>/contact/<int:arg_1>/update',view_func=update_contact,methods=['GET','POST'])
app.add_url_rule('/customer/<int:arg_0>/contacts',view_func=list_contacts)


if __name__=='__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--port',type=int,default=2000)
  parser.add_argument('--host',default='0.0.0.0')
  args = parser.parse_args()
  try:
    print 'Starting SloopStash CRM app service...'
    app.run(debug=True,host=args.host,port=args.port)
  except KeyboardInterrupt:
    print 'Stopping SloopStash CRM app service...'
  finally:
    pass
