from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


real_user = User.objects.get(username = 'ahmad@gmail.com')

class LoginViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='ahmad@gmail.com', email='ahmad@gmail.com', password='123456')

    def test_is_in_database(self):
        
        self.assertEqual(real_user.first_name,'fa')
        self.assertTrue(check_password('123456', real_user.password))

    def test_login_successful(self):
        response = self.client.post(reverse('login'), {
            'email': 'ahmad@gmail.com',
            'password': '123456'
        })
        self.assertRedirects(response, reverse('mainPage'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid Email or Password')  # Match the exact string used in views

    def test_get_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'logPage.html')

    def test_authenticated_user_redirected_from_login(self):
        self.client.login(username='ahmad@gmail.com', password='123456')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('mainPage'))

