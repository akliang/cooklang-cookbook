from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class LoginLogoutRegisterTests(TestCase):
  username = "testuser123456"
  password = "98vbzlkqb3lahsfdpo87"

  def setUp(self):
    user = User.objects.create_user(username=self.username, password=self.password)

  def test_homepage_while_anonymous(self):
    response = self.client.get('/')
    self.assertRedirects(response, reverse("web:login"))

  def test_login_while_anonymous(self):
    response = self.client.get('/login/')
    self.assertEquals(response.status_code, 200)

  def test_logout_while_anonymous(self):
    response = self.client.get('/logout/', follow=True)
    self.assertRedirects(response, reverse("web:login"))

  def test_recipe_while_anonymous(self):
    response = self.client.get('/recipe/', follow=True)
    self.assertRedirects(response, f'{reverse("web:login")}?next=%2Frecipe%2F')

  def test_recipe_view_while_anonymous(self):
    response = self.client.get(f'/v/{self.username}/test_recipe')
    self.assertEquals(response.status_code, 200)

  def test_homepage_while_logged_in(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get('/')
    self.assertEquals(response.status_code, 200)

  def test_login_while_logged_in(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get('/login/', follow=True)
    self.assertRedirects(response, reverse("web:index"))

  def test_logout_while_logged_in(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get('/logout/', follow=True)
    self.assertRedirects(response, reverse("web:login"))

  def test_recipe_while_logged_in(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get('/recipe/')
    self.assertEquals(response.status_code, 200)

  def test_view_while_logged_in(self):
    self.client.login(username=self.username, password=self.password)
    response = self.client.get(f'/v/{self.username}/test_recipe')
    self.assertEquals(response.status_code, 200)

