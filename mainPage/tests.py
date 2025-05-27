from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product
from decimal import Decimal


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



class ProductSearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Medicine")

        # Create a test image file
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )

        # Create test products with the image
        self.p1 = Product.objects.create(
            name="Aspirin",
            price=Decimal('10.00'),
            category=self.category,
            image=test_image,
            count=10,
            available=True
        )
        self.p2 = Product.objects.create(
            name="Paracetamol",
            price=Decimal('8.00'),
            category=self.category,
            image=test_image,
            count=10,
            available=True
        )
        self.p3 = Product.objects.create(
            name="Ibuprofen",
            price=Decimal('12.00'),
            category=self.category,
            image=test_image,
            count=10,
            available=True
        )

    def test_search_exact_match(self):
        response = self.client.get(reverse('search'), {'q': 'Aspirin'})
        self.assertContains(response, "Aspirin")
        self.assertNotContains(response, "Paracetamol")
        self.assertNotContains(response, "Ibuprofen")

    def test_search_case_insensitive(self):
        response = self.client.get(reverse('search'), {'q': 'aspirin'})
        self.assertContains(response, "Aspirin")

    def test_search_partial_match(self):
        response = self.client.get(reverse('search'), {'q': 'para'})
        self.assertContains(response, "Paracetamol")

    def test_search_no_results(self):
        response = self.client.get(reverse('search'), {'q': 'VitaminC'})
        self.assertContains(response, "No products found")

    def test_search_empty_query(self):
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertNotContains(response, "Aspirin")
        self.assertContains(response, "No products found")

    def test_search_special_characters(self):
        response = self.client.get(reverse('search'), {'q': '@#$%'})
        self.assertContains(response, "No products found")

    def test_search_multiple_results(self):
        response = self.client.get(reverse('search'), {'q': 'i'})
        self.assertContains(response, "Aspirin")
        self.assertContains(response, "Ibuprofen")

        response = self.client.get(reverse('search'), {'q': 'mol'})
        self.assertContains(response, "Paracetamol")
       

