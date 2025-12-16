from django.urls import path
from .views_api import (
    health_check,
    RestaurantListAPIView,
    RestaurantDetailAPIView,
    restaurant_search,
    CuisineTypeListAPIView,
)

urlpatterns = [
    # Health Check
    path('health/', health_check, name='api_health_check'),
    
    # Рестораны
    path('restaurants/', RestaurantListAPIView.as_view(), name='api_restaurant_list'),
    path('restaurants/<int:pk>/', RestaurantDetailAPIView.as_view(), name='api_restaurant_detail'),
    path('restaurants/search/', restaurant_search, name='api_restaurant_search'),
    
    # Типы кухонь
    path('cuisines/', CuisineTypeListAPIView.as_view(), name='api_cuisine_list'),
]