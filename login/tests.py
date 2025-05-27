from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class LoginViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='ahmad@gmail.com',
            email='ahmad@gmail.com',
            password='123456',
            first_name='fa3'  # Set the first name here
        )

    def test_is_in_database(self):
        user = User.objects.get(username='ahmad@gmail.com')
        self.assertEqual(user.first_name, 'fa3')
        self.assertTrue(check_password('123456', user.password))

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


class SignupViewTest(TestCase):

    def test_signup_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logPage.html')

    def test_successful_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse('register'), {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        })

      
        user_exists = User.objects.filter(email='testuser@example.com').exists()
        self.assertTrue(user_exists)
        self.assertRedirects(response, reverse('login'))

    def test_signup_fails_if_user_already_exists(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='testpassword')

        response = self.client.post(reverse('register'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'anotherpassword',
        })

        self.assertEqual(User.objects.filter(email='test@example.com').count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logPage.html')
        self.assertContains(response, "Email already exists")


