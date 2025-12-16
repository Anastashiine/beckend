from django.db import models
from restaurants.models import Restaurant
from users.models import CustomUser

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        unique_together = ['user', 'restaurant']  
    def __str__(self):
        return f"Отзыв от {self.user.username} - {self.rating} звезд"