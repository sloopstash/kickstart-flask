# Import community modules. 
import sys
import json
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask,request,render_template
from werkzeug.exceptions import NotFound,BadRequest
import argparse
from flask import jsonify,render_template,redirect

# Append App specific Python paths.
sys.path.append('includes')
sys.path.append('core')

# Import custom modules.
from database import redis
from config import app_conf, redis_conf

# Intialize App.
app = Flask('CRM App',template_folder='templates')

app.config['ELASTIC_APM'] = {
  # Set required service name. Allowed characters:
  # a-z, A-Z, 0-9, -, _, and space
  'SERVICE_NAME': 'CRM App',

  # Use if APM Server requires a token
  'SECRET_TOKEN': '',

  # Set custom APM Server URL (default: http://localhost:8200)
  'SERVER_URL': 'http://elk-apm:8200',
  'DEBUG': True
}

apm = ElasticAPM(app,logging=True)

@app.route('/health',methods=['GET'])
def health():
  return 'OK'

@app.route('/dashboard',methods=['GET'])
def home():
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  vars['accounts'] = redis.engine.hgetall(redis_conf['key_prefix']['account'])
  for key,value in vars['accounts'].items():
    vars['accounts'][key] = json.loads(value)
  return render_template('dashboard.html',vars=vars)

@app.route('/account/create',methods=['GET','POST'])
def account_create():
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    return render_template('account/create.html',vars=vars)
  elif request.method=='POST':
    data = {}
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    data['organization'] = request.form['organization']
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    id = redis.engine.incr(redis_conf['key_prefix']['account_counter'])
    response = redis.engine.hset(redis_conf['key_prefix']['account'],id,json.dumps(data))
    if response:
      return redirect('/dashboard')
    else:
      vars['message'] = 'Failure'
      return render_template('account/create.html',vars=vars)

@app.route('/account/<id>/update',methods=['GET','POST'])
def account_update(id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],id))
    vars['account']['id'] = id
    return render_template('account/update.html',vars=vars)
  elif request.method=='POST':
    data = {}
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    data['organization'] = request.form['organization']
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    response = redis.engine.hset(redis_conf['key_prefix']['account'],id,json.dumps(data))
    return redirect('/dashboard')

@app.route('/account/<id>/view',methods=['GET'])
def account_view(id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],id))
  vars['account']['id'] = id
  return render_template('account/view.html',vars=vars)

@app.route('/account/<act_id>/contacts',methods=['GET'])
def contact_view(act_id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
  vars['account']['id'] = act_id
  vars['contacts'] = redis.engine.hgetall(redis_conf['key_prefix']['contact']+':'+str(act_id))
  for key,value in vars['contacts'].items():
    vars['contacts'][key] = json.loads(value)
  return render_template('contact/view.html',Active='contacts',vars=vars)

@app.route('/account/<act_id>/contact/create',methods=['GET','POST'])
def contact_create(act_id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
    vars['account']['id'] = act_id
    return render_template('contact/create.html',Active='contacts',vars=vars)
  elif request.method=='POST':
    data = {}
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    id = redis.engine.incr(redis_conf['key_prefix']['contact_counter']+':'+str(act_id))
    response = redis.engine.hset(redis_conf['key_prefix']['contact']+':'+str(act_id),id,json.dumps(data))
    if response:
      return redirect('/account/'+act_id+'/contacts')
    else:
      vars['message'] = 'Failure'
      return render_template('contact/create.html',Active='contacts',vars=vars)

@app.route('/account/<act_id>/contact/<id>/update',methods=['GET','POST'])
def contact_update(act_id,id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
    vars['account']['id'] = act_id
    vars['contact'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['contact']+':'+str(act_id),id))
    vars['contact']['id'] = id
    return render_template('contact/update.html',Active='contacts',vars=vars)
  elif request.method=='POST':
    data = {}
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    response = redis.engine.hset(redis_conf['key_prefix']['contact']+':'+str(act_id),id,json.dumps(data))
    return redirect('/account/'+act_id+'/contacts')

@app.route('/account/<act_id>/leads',methods=['GET'])
def lead_view(act_id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
  vars['account']['id'] = act_id
  vars['leads'] = redis.engine.hgetall(redis_conf['key_prefix']['lead']+':'+str(act_id))
  for key,value in vars['leads'].items():
    vars['leads'][key] = json.loads(value)  
  return render_template('lead/view.html',Active='leads',vars=vars)

@app.route('/account/<act_id>/lead/create',methods=['GET','POST'])
def lead_create(act_id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
    vars['account']['id'] = act_id
    return render_template('lead/create.html',Active='leads',vars=vars)
  elif request.method=='POST':
    data = {}
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    id = redis.engine.incr(redis_conf['key_prefix']['lead_counter']+':'+str(act_id))
    response = redis.engine.hset(redis_conf['key_prefix']['lead']+':'+str(act_id),id,json.dumps(data))
    if response:
      return redirect('/account/'+act_id+'/leads')
    else:
      vars['message'] = 'Failure'
      return render_template('lead/create.html',Active='leads',vars=vars)

@app.route('/account/<act_id>/lead/<id>/update',methods=['GET','POST'])
def lead_update(act_id,id):
  vars = {}
  vars['environment'] = app_conf['environment']
  vars['cdn'] = app_conf['cdn']
  if request.method=='GET':
    vars['account'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['account'],act_id))
    vars['account']['id'] = act_id
    vars['lead'] = json.loads(redis.engine.hget(redis_conf['key_prefix']['lead']+':'+str(act_id),id))
    vars['lead']['id'] = id
    return render_template('lead/update.html',Active='leads',vars=vars)
  elif request.method=='POST':
    data = {}
    data['email'] = request.form['email']
    data['phone'] = request.form['phone']
    data['firstname'] = request.form['firstname']
    data['lastname'] = request.form['lastname']
    response = redis.engine.hset(redis_conf['key_prefix']['lead']+':'+str(act_id),id,json.dumps(data))
    return redirect('/account/'+act_id+'/leads')

if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--port','-P',type=int,default=5000)
    parser.add_argument('--host','-H',default='0.0.0.0')
    args = parser.parse_args()
    print('starting app')
    app.run(debug=False,host=args.host,port=args.port)
  except KeyboardInterrupt:
    print('stopping app')
