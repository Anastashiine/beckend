from rest_framework import serializers
from .models import Restaurant, CuisineType

class CuisineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuisineType
        fields = ['id', 'name']

class RestaurantSerializer(serializers.ModelSerializer):
    cuisine_type = CuisineTypeSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'metro_station', 
            'average_bill', 'cuisine_type', 'phone', 
            'schedule', 'image_url', 'created_at'
        ]