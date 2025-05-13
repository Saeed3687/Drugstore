from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cart, CartItem
from mainPage.models import Product, Category
from userProfile.models import UserProfile
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from parameterized import parameterized

class CartTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create user profile
        self.profile = UserProfile.objects.create(
            user=self.user,
            address='Test Address',
            phone_number='1234567890'
        )
        
        # Create test category
        self.category = Category.objects.create(name='Test Category')
        
        # Create test products with dummy image
        dummy_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        self.product1 = Product.objects.create(
            name='Test Product 1',
            price=Decimal('10.00'),
            category=self.category,
            image=dummy_image
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=Decimal('20.00'),
            category=self.category,
            image=dummy_image
        )
        
        # Create client and login
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertFalse(cart.is_paid)
        self.assertEqual(cart.get_total_price(), Decimal('0'))

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product1,
            quantity=2,
            price=self.product1.price
        )
        self.assertEqual(cart_item.get_cost(), Decimal('20.00'))
        self.assertEqual(cart.get_total_price(), Decimal('20.00'))

    def test_add_to_cart_view(self):
        response = self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after adding
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product1)

    def test_add_same_product_twice(self):
        # Add product twice
        self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_from_cart(self):
        # First add an item
        response = self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        
        # Then remove it
        response = self.client.get(reverse('remove_from_cart', args=[cart_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(cart.items.count(), 0)

    def test_update_quantity(self):
        # Add item to cart
        self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        
        # Update quantity
        response = self.client.post(reverse('update_quantity', args=[cart_item.id]), {'quantity': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.get_cost(), Decimal('30.00'))

    def test_view_cart(self):
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'My-Cart.html')

    @parameterized.expand([
        ("single_product", [(1, '10.00', 2)], '20.00'),
        ("two_products", [(1, '10.00', 2), (2, '20.00', 1)], '40.00'),
        ("empty_cart", [], '0.00'),
        ("multiple_quantities", [(1, '10.00', 5), (2, '20.00', 3)], '110.00'),
    ])
    def test_cart_total_price(self, name, items, expected_total):
        cart = Cart.objects.create(user=self.user)
        
        # Add items to cart based on test parameters
        for product_num, price, quantity in items:
            product = self.product1 if product_num == 1 else self.product2
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=Decimal(price)
            )
        
        self.assertEqual(cart.get_total_price(), Decimal(expected_total))

    def test_cart_requires_login(self):
        # Logout the user
        self.client.logout()
        
        # Try to access cart views
        cart_urls = ['view_cart', 'proceed_to_checkout', 'payment']
        for url in cart_urls:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/login/'))

    @parameterized.expand([
        ("increase_quantity", 1, 3, Decimal('30.00')),  # Increase from 1 to 3
        ("decrease_quantity", 5, 2, Decimal('20.00')),  # Decrease from 5 to 2
        ("min_quantity", 3, 1, Decimal('10.00')),      # Decrease to minimum
        ("same_quantity", 2, 2, Decimal('20.00')),     # No change
    ])
    def test_cart_item_quantity_updates(self, name, initial_qty, new_qty, expected_total):
        # Create cart and add item with initial quantity
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product1,
            quantity=initial_qty,
            price=self.product1.price
        )
        
        # Update quantity
        response = self.client.post(
            reverse('update_quantity', args=[cart_item.id]),
            {'quantity': new_qty}
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        
        # Refresh from database and verify
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, new_qty)
        self.assertEqual(cart_item.get_cost(), expected_total)

    def test_proceed_to_checkout(self):
        # Add item to cart
        self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        
        # Test GET request
        response = self.client.get(reverse('proceed_to_checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proceed-checkout.html')
        
        # Test POST request
        checkout_data = {
            'fullName': 'Test User',
            'address': '123 Test St',
            'phone': '1234567890',
            'zipCode': '12345'
        }
        response = self.client.post(reverse('proceed_to_checkout'), checkout_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment'))

    def test_payment_process(self):
        # Add item to cart
        self.client.get(reverse('add_to_cart', args=[self.product1.id]))
        cart = Cart.objects.get(user=self.user)
        
        # Test GET request to payment page
        response = self.client.get(reverse('payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pay.html')
        
        # Test POST request (simulating payment)
        response = self.client.post(reverse('payment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_orders'))
        
        # Verify cart is marked as paid
        cart.refresh_from_db()
        self.assertTrue(cart.is_paid)
        
        # Verify order was created
        from userProfile.models import Order
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, cart.get_total_price())
        self.assertEqual(order.items.count(), cart.items.count())
