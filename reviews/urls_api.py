from django.urls import path
from .views_api import (
    ReviewCreateAPIView,
    UserReviewsAPIView,
    RestaurantReviewsAPIView,
    ReviewDetailAPIView,
    restaurant_stats
)

urlpatterns = [
    path('reviews/', ReviewCreateAPIView.as_view(), name='api_review_create'),
    path('reviews/my/', UserReviewsAPIView.as_view(), name='api_user_reviews'),
    path('reviews/restaurant/<int:restaurant_id>/', RestaurantReviewsAPIView.as_view(), name='api_restaurant_reviews'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='api_review_detail'),
    path('restaurants/<int:restaurant_id>/stats/', restaurant_stats, name='api_restaurant_stats'),
]