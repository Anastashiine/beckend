from django.urls import path
from .views_api import (
    BookingCreateAPIView, 
    UserBookingsAPIView, 
    BookingDetailAPIView, 
    cancel_booking
)

urlpatterns = [
    path('bookings/', BookingCreateAPIView.as_view(), name='api_booking_create'),
    path('bookings/my/', UserBookingsAPIView.as_view(), name='api_user_bookings'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='api_booking_detail'),
    path('bookings/<int:pk>/cancel/', cancel_booking, name='api_booking_cancel'),
]