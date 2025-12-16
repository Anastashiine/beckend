from rest_framework import serializers
from .models import Booking
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'restaurant', 'booking_date', 'booking_time', 'guests_count', 'special_requests']
        extra_kwargs = {
            'user': {'read_only': True},
            'status': {'read_only': True}
        }

    def validate_guests_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество гостей должно быть не менее 1")
        if value > 20:
            raise serializers.ValidationError("Максимальное количество гостей - 20")
        return value

class BookingSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), 
        source='restaurant', 
        write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'restaurant', 'restaurant_id', 'booking_date', 'booking_time', 
            'guests_count', 'special_requests', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']