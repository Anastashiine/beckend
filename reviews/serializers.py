from rest_framework import serializers
from .models import Review
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer

class ReviewSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), 
        source='restaurant', 
        write_only=True
    )
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'restaurant', 'restaurant_id', 'user_name', 'rating', 
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        restaurant = attrs['restaurant']
        
        # Проверяем, есть ли уже отзыв от этого пользователя на этот ресторан
        if Review.objects.filter(user=user, restaurant=restaurant).exists():
            if not self.instance:  # Только при создании нового отзыва
                raise serializers.ValidationError("Вы уже оставляли отзыв для этого ресторана")
        
        return attrs