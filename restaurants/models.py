from django.db import models
from users.models import CustomUser

class CuisineType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    metro_station = models.CharField(max_length=100)
    average_bill = models.DecimalField(max_digits=10, decimal_places=2)
    cuisine_type = models.ForeignKey(CuisineType, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    schedule = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

