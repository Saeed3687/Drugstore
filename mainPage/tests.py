from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product


class MainPageViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user@example.com', password='pass123')

        self.category = Category.objects.create(name="Painkillers")
        self.product = Product.objects.create(
            name="Paracetamol",
            image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
            price=10.0,
            rating=0.0,
            num_ratings=0,
            category=self.category
        )

    def test_main_page_loads(self):
        response = self.client.get(reverse('mainPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainPage.html')
        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)

    def test_category_products_view(self):
        response = self.client.get(reverse('category_products', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertIn(self.product, response.context['products'])

    
    def test_user_profile_requires_login(self):
        response = self.client.get(reverse('user_profile'))
        self.assertRedirects(response, f"/login/?next={reverse('user_profile')}")

    def test_user_profile_authenticated(self):
        self.client.login(username='user@example.com', password='pass123')
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')
        self.assertEqual(response.context['user'], self.user)
