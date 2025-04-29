from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            password='testpass123',
            first_name='TestUser'
        )

    def test_user_profile_requires_login(self):
        response = self.client.get(reverse('user_profile'))
        self.assertRedirects(response, f"/login/?next={reverse('user_profile')}")

    

    def test_update_user_info_success(self):
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': 'new@example.com',
            'username': 'NewName'
        })
        self.assertRedirects(response, reverse('user_profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')
        self.assertEqual(self.user.first_name, 'NewName')

    def test_update_user_info_duplicate_email_fails(self):
        # Another user exists with same email
        User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='otherpass'
        )

        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': 'other@example.com',
            'username': 'NewName'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already exists')

    def test_update_user_info_missing_fields(self):
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': '',
            'username': ''
        })
        self.user.refresh_from_db()
       
        self.assertEqual(self.user.email, 'user@example.com')
        self.assertEqual(self.user.first_name, 'TestUser')
