from rest_framework import serializers
from .models import Favourite
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer

class FavouriteSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), 
        source='restaurant', 
        write_only=True
    )

    class Meta:
        model = Favourite
        fields = ['id', 'restaurant', 'restaurant_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        restaurant = attrs['restaurant']
        
        # Проверяем, есть ли уже этот ресторан в избранном
        if Favourite.objects.filter(user=user, restaurant=restaurant).exists():
            if not self.instance:
                raise serializers.ValidationError("Этот ресторан уже в избранном")
        
        return attrs