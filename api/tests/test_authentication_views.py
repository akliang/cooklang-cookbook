from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class TestAuthenticationViews(TestCase):
  username = "testuser123456"
  username2 = "testuser123456789"
  password = "98vbzlkqb3lahsfdpo87"
  new_password = "98vbzlkqb3lahsfdpo87444"
  email = "test@test.com"

  def setUp(self):
    user = User.objects.create_user(username=self.username, password=self.password)

  def test_api_login(self):
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': self.password})
    self.assertEqual(response.status_code, 200)
    self.assertTrue('token' in response.json())

  def test_api_login_incorrect(self):
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': 'incorrect'})
    self.assertEqual(response.status_code, 401)

  def test_api_register_and_delete(self):
    response = self.client.post('/api/api_register/', {'username': self.username2, 'password1': self.password, 'password2': self.password, 'email': self.email})
    self.assertEqual(response.status_code, 200)
    self.assertTrue(self.username2 in response.json())
    # login first to get API key
    response = self.client.post('/api/api_login/', {'username': self.username2, 'password': self.password})
    response = self.client.post('/api/api_delete/', {}, HTTP_AUTHORIZATION=f'token {response.json()["token"]}')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(self.username2, response.json()['username'])

  def test_api_changepw(self):
    # login first to get API key
    response = self.client.post('/api/api_login/', {'username': self.username, 'password': self.password})
    response = self.client.post('/api/api_changepw/', {'username': self.username, 'old_password': self.password, 'new_password1': self.new_password, 'new_password2': self.new_password}, HTTP_AUTHORIZATION=f'token {response.json()["token"]}')
    self.assertEqual(response.status_code, 200)
    self.assertTrue('Password updated' in response.data)



