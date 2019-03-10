from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, resolve
from django.test import TestCase
from .views import signup

class SingUpTests(TestCase):
    def test_singup_view_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_signup_url_resovles_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)



class SucessfulSingUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'luka',
            'password1': 'banane12',
            'password2': 'banane12'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redrection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)




class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


