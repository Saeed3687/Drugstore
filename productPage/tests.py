from django.test import TestCase, Client
from django.urls import reverse
from mainPage.models import Product, Category, Comment
from django.core.files.uploadedfile import SimpleUploadedFile
from parameterized import parameterized
from django.contrib.auth.models import User


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
            image=image
        )
        self.url = reverse('rate_product', args=[self.product.id])
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    def test_rating_updated(self):
        response = self.client.post(self.url, {'rating': '5'})
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertAlmostEqual(self.product.rating, (4.0 + 5.0) / 2)

    def test_num_ratings_updated(self):
        response = self.client.post(self.url, {'rating': '5'})
        self.product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.num_ratings, 2)

    def test_url_works(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")





class RateProductTestsParameterized(TestCase):
    def setUp(self):
        image = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        self.product = Product.objects.create(name='Test Product', price=10.00, image=image)
        self.url = reverse('rate_product', args=[self.product.id])
        self.user = User.objects.create_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

    @parameterized.expand([
        ("valid_rating_1", 1, True,),
        ("valid_rating_3", 3, True,),
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

    @parameterized.expand([
        ("rates1", [1,2,3] ,2),
        ("rates2", [5,3,4] ,4),
    ])
    def test_rating_updated(self, name, rates, True_rate):
        # Create a new user for each rating to simulate different users rating the product
        for i, rate in enumerate(rates):
            user = User.objects.create_user(username=f'user{i}', password='pass')
            self.client.login(username=f'user{i}', password='pass')
            response = self.client.post(self.url, {'rating': rate})
            self.product.refresh_from_db()
            self.assertEqual(response.status_code, 302)  # Should redirect

        self.assertAlmostEqual(self.product.rating, True_rate)


class commentandrep(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.product = Product.objects.create(name="Test Product", price=10.99, category=self.category, image=image)
        self.user = User.objects.create_user(username='ahmad', password='12345')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

    def test_user_can_add_comment(self):
        self.client.login(username='ahmad', password='12345')
        url = reverse('add_comment', args=[self.product.id])
        response = self.client.post(url, {'comment': 'Great product!'})
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(product=self.product)
        self.assertEqual(comment.text, 'Great product!')
        self.assertEqual(comment.user, self.user)




