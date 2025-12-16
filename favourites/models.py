from django.db import models
from users.models import CustomUser
from restaurants.models import Restaurant

class Favourite(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='user_favourites'  # ← ДОБАВЬТЕ related_name
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE,
        related_name='restaurant_favourites'  # ← ДОБАВЬТЕ related_name
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'restaurant']
    
    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"