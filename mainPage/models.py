from django.db import models

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
    available = models.BooleanField(default=True)  # Add this field


    def update_rating(self, new_rating):
        """Update the product's rating when a new rating is submitted."""
        total_rating = self.rating * self.num_ratings + new_rating
        self.num_ratings += 1
        self.rating = total_rating / self.num_ratings
        self.save()

    def __str__(self):
        return self.name


