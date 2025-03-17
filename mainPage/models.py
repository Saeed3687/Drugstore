from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/images/products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0.0)  # Store average rating
    num_ratings = models.IntegerField(default=0)  # Track number of ratings
   
    def update_rating(self, new_rating):
        """Update the product's rating when a new rating is submitted."""
        total_rating = self.rating * self.num_ratings + new_rating
        self.num_ratings += 1
        self.rating = total_rating / self.num_ratings
        self.save()

    def __str__(self):
        return self.name
