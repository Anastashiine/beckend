from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('restaurants.urls_api')),
    path('api/', include('users.urls_api')),
    path('api/', include('bookings.urls_api')),
    path('api/', include('reviews.urls_api')),
    path('api/', include('favourites.urls_api')), 
    
    # REST Framework auth
    path('api-auth/', include('rest_framework.urls')),
]