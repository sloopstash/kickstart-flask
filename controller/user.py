##
# -*- coding: utf-8 -*-
##
##
# User controller.
##

# Import community modules.
from flask import render_template, redirect, request, flash, make_response, session

# Import custom modules.
from controller import root_web_controller
from model.user import user

# User web controller.
class user_web_controller(root_web_controller):

  # HTTP GET method processor.
  def get(self, *args, **kwargs):
    if self.request.path == '/login':
      return render_template('user/login.html', var=self.var)
    elif self.request.path == '/signup':
      return render_template('user/signup.html', var=self.var)
    elif self.request.path == '/dashboard':
      user_id = self._get_authenticated_user_id()
      if user_id:
        user_data = user().get(user_id)
        if user_data:
          self.var['user'] = user_data
          return render_template('user/dashboard.html', var=self.var)
      return redirect('/login')
    elif self.request.path == '/logout':
      return self.logout()
    else:
      return render_template('error.html', var=self.var)  

  # HTTP POST method processor.
  def post(self):
    if self.request.path == '/login':
      username = self.request.form.get('username')
      password = self.request.form.get('password')
      user_model = user()
      user_data = user_model.authenticate(username, password)

      if user_data:
        if user_model.authenticate(username, password):
          session['user_id'] = user_data['id']  
          session['username'] = user_data['username']
          return redirect('/dashboard')
        else:
          flash("Invalid username or password", "error")   
          self.var = {'static': {'endpoint': 'your_static_endpoint_url'}}
          self.var['show_signup_link'] = True
          return render_template('user/login.html', error="Invalid username or password", var=self.var)
      else:
        flash("Don't have an account? Sign up first.", "info")
        return redirect('/login')
    elif self.request.path == '/signup':
      username = self.request.form.get('username')
      email = self.request.form.get('email')
      password = self.request.form.get('password')
      confirm_password = self.request.form.get('confirm-password')
      if password != confirm_password:
        flash("Passwords do not match", "error")
        return render_template('user/signup.html', error="Passwords do not match", var=self.var)
      user_model = user()
      user_id = user_model.create(username, password, email)
      if user_id:
        flash("Signup successful. Please login.", "success")
        return redirect('/login')  
      else:
        flash("Signup failed. Please try again.", "error")
        return render_template('user/signup.html', error="Signup failed", var=self.var)
    return render_template('error.html', var=self.var)


  def _set_authenticated_user(self, user_id):
    resp = make_response(redirect('/dashboard'))
    resp.set_cookie('user_id', str(user_id), max_age=60*60*24*30)  
    return resp

  def _get_authenticated_user_id(self):
    user_id = self.request.cookies.get('user_id')
    if user_id:
      return user_id
    user_id = session.get('user_id')
    return user_id if user_id else None

  # Method to handle logout
  def logout(self):
    resp = make_response(redirect('/login'))  
    resp.delete_cookie('user_id')  
    session.clear() 
    return resp
