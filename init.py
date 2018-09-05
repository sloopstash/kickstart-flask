
# import argparse

# app = Flask(__name__)
# app.config['ELASTIC_APM'] = {
#    'SERVICE_NAME': 'Sample App',
#    'SECRET_TOKEN': 'test123',
# }
# apm = ElasticAPM(app)


# import community modules. 
import sys
from flask import Flask,request,render_template
from werkzeug.exceptions import NotFound,BadRequest
import argparse
from flask import jsonify,render_template

# append app specific python paths.
sys.path.append('includes')
sys.path.append('core')

# import custom modules.
from database import redis
from common import text_validate
from contact import contact

# intialize flask app.
app = Flask('dws app',template_folder='templates')

# Home
@app.route('/dashboard',methods=['GET'])
def home():
  return render_template('dashboard.html')

@app.route('/account/view',methods=['GET'])
def account_view():
  return render_template('account/view.html')

@app.route('/account/create',methods=['GET','POST'])
def account_create():
  return render_template('account/create.html')

@app.route('/account/update',methods=['GET','POST'])
def account_update():
  return render_template('account/update.html')

@app.route('/contact/view',methods=['GET'])
def contact_view():
  return render_template('contact/view.html',Active='contacts')

@app.route('/contact/create',methods=['GET','POST'])
def contact_create():
  return render_template('contact/create.html',Active='contacts')

@app.route('/contact/update',methods=['GET','POST'])
def contact_update():
  return render_template('contact/update.html',Active='contacts')

@app.route('/lead/view',methods=['GET'])
def lead_view():
  return render_template('lead/view.html',Active='leads')

@app.route('/lead/create',methods=['GET','POST'])
def lead_create():
  return render_template('lead/create.html',Active='leads')

@app.route('/lead/update',methods=['GET','POST'])
def lead_update():
  return render_template('lead/update.html',Active='leads')

if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--port','-P',type=int,default=5000)
    parser.add_argument('--host','-H',default='0.0.0.0')
    args = parser.parse_args()
    print 'starting app'
    app.run(debug=True,host=args.host,port=args.port)
  except KeyboardInterrupt:
    print 'stopping app'
