# Import community modules. 
import sys
import pytest

# Append App specific Python paths.
sys.path.append('./')

# Import custom modules.
from init import app

# Initialize the App test client.
@pytest.fixture(scope='module')
def client():
  app_client = app.test_client()
  app_context = app.app_context()
  app_context.push()
  yield app_client
  app_context.pop()

# Test health check.
def test_health_check(client):
  response = client.get('/health')
  assert response.status_code == 200
  assert response.data == 'OK'
  print "Test : Health check - passed"

# Test dashboard view.
def test_dashboard(client):
  response = client.get('/dashboard')
  assert response.status_code == 200
  print "Test : Dashboard view - passed"

# Test account create view.
def test_account_create(client):
  response = client.get('/account/create')
  assert response.status_code == 200
  print "Test : Account create view - passed"
