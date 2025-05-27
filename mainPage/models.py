from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='static/images/categories/', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def products(self):
        return self.product_set.all()  # Returns all products in this category


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images/products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0.0)  # Store average rating
    num_ratings = models.IntegerField(default=0)  # Track number of ratings
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    count = models.IntegerField(default=0)  # Add count field
    available = models.BooleanField(default=True)  # Add this field

    def update_rating(self, user, new_rating):
        """Update the product's rating when a new rating is submitted."""
        # Get or create user rating
        user_rating, created = UserRating.objects.get_or_create(
            user=user,
            product=self,
            defaults={'rating': new_rating}
        )

        if not created:
            # If rating exists, update it
            old_rating = user_rating.rating
            user_rating.rating = new_rating
            user_rating.save()
            
            # Update product rating by subtracting old rating and adding new rating
            total_rating = (self.rating * self.num_ratings) - old_rating + new_rating
            self.rating = total_rating / self.num_ratings
        else:
            # If new rating, add to total
            total_rating = (self.rating * self.num_ratings) + new_rating
            self.num_ratings += 1
            self.rating = total_rating / self.num_ratings
        
        self.save()
        return user_rating

    def get_user_rating(self):
        """Get the current user's rating for this product."""
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            # Get the current user from the request
            from django.contrib.auth.context_processors import auth
            request = auth(None).get('request')
            if request and not isinstance(request.user, AnonymousUser):
                return UserRating.objects.get(user=request.user, product=self).rating
        except (UserRating.DoesNotExist, AttributeError):
            return None
        return None

    def update_availability(self):
        """Update product availability based on count"""
        self.available = self.count > 0
        self.save()

    def decrease_count(self, amount=1):
        """Decrease product count and update availability"""
        if self.count >= amount:
            self.count -= amount
            self.update_availability()
            return True
        return False

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)  # Admin reply

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.first_name} on {self.product.name}'


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']  # Ensure one rating per user per product

    def __str__(self):
        return f'{self.user.first_name} rated {self.product.name} as {self.rating}'


