from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile  # adjust app name if different

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            password='testpass123',
            first_name='TestUser'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='123 Main St',
            phone_number='+989123456789'
        )


    def test_user_profile_requires_login(self):
        response = self.client.get(reverse('user_profile'))
        self.assertRedirects(response, f"/login/?next={reverse('user_profile')}")

    def test_user_profile_view_displays_info(self):
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.get(reverse('user_info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestUser')
        self.assertContains(response, 'user@example.com')
        self.assertContains(response, '123 Main St')
        self.assertContains(response, '+989123456789')

    def test_update_user_info_success(self):
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': 'new@example.com',
            'username': 'NewName',
            'address': '456 New St',
            'phone_number': '+989111112222'
        })
        self.assertRedirects(response, reverse('user_info'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')
        self.assertEqual(self.user.first_name, 'NewName')
        self.assertEqual(self.profile.address, '456 New St')
        self.assertEqual(self.profile.phone_number, '+989111112222')

    def test_update_user_info_duplicate_email_fails(self):
        User.objects.create_user(
            username='other@example.com',
            email='other@example.com',
            password='otherpass'
        )
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': 'other@example.com',
            'username': 'NewName',
            'address': 'Test',
            'phone_number': '+989000000000'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already in use by another account')

    def test_update_user_info_missing_fields(self):
        self.client.login(username='user@example.com', password='testpass123')
        response = self.client.post(reverse('update_user_info'), {
            'email': '',
            'username': '',
            'address': '',
            'phone_number': ''
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.email, 'user@example.com')
        self.assertEqual(self.user.first_name, 'TestUser')
        self.assertNotEqual(self.profile.address, '')
        self.assertNotEqual(self.profile.phone_number, '')
