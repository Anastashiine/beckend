from django.urls import path
from .views_api import (
    FavouriteCreateAPIView,
    UserFavouritesAPIView,
    remove_favourite,
    check_favourite
)

urlpatterns = [
    path('favourites/', FavouriteCreateAPIView.as_view(), name='api_favourite_create'),
    path('favourites/my/', UserFavouritesAPIView.as_view(), name='api_user_favourites'),
    path('favourites/check/<int:restaurant_id>/', check_favourite, name='api_check_favourite'),
    path('favourites/remove/<int:restaurant_id>/', remove_favourite, name='api_remove_favourite'),
]