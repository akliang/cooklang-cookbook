from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginLogoutRegisterTests(TestCase):
  username = "testuser123456"
  password = "98vbzlkqb3lahsfdpo87"

  def setUp(self):
    user = User.objects.create_user(username=self.username, password=self.password)

  def test_api_login(self):
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': self.password})
    self.assertEqual(response.status_code, 200)
    self.assertTrue('token' in response.json())

  def test_api_login_incorrect(self):
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': 'incorrect'})
    self.assertEqual(response.status_code, 401)

  def test_register(self):
    response = self.client.post('/api/register/', {'username': self.username, 'password': 'incorrect'})