
from django.test import TestCase, Client
from django.urls import reverse
from mainPage.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.
class RateProductViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=10.99,
            rating=4.0,
            num_ratings=1,
            category=self.category,
            image = image
        )
        self.url = reverse('rate_product', args=[self.product.id])  # You must have named your url 'rate_product'

    def test_rating_updated(self):
        response = self.client.post(self.url, {'rating': '5'})
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Should redirect

        self.assertAlmostEqual(self.product.rating, (4.0 + 5.0) / 2)

    def test_num_ratings_updated(self):
        response = self.client.post(self.url, {'rating': '5'})
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertEqual(self.product.num_ratings, 2)

    def test_url_works(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

from parameterized import parameterized


class RateProductViewTests(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        self.product = Product.objects.create(name='Test Product', price=10.00, image=image)
        self.url = reverse('rate_product', args=[self.product.id])

    @parameterized.expand([
        ("valid_rating_1", 1, True),
        ("valid_rating_3", 3, True),
        ("valid_rating_5", 5, True),
        ("invalid_rating_0", 0, False),
        ("invalid_rating_6", 6, False),
        
    ])
    def test_rating_submission(self, name, rating_value, should_update):
        response = self.client.post(self.url, {'rating': rating_value})
        self.product.refresh_from_db()

        if should_update:
            self.assertEqual(response.status_code, 302)  # should redirect
            self.assertGreater(self.product.rating, 0)
            self.assertEqual(self.product.num_ratings, 1)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.product.rating, 0)
            self.assertEqual(self.product.num_ratings, 0)
