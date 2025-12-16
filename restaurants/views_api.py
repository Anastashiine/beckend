from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, CuisineType
from .serializers import RestaurantSerializer, CuisineTypeSerializer

# Health Check Endpoint
@api_view(['GET'])
def health_check(request):
    """Простой endpoint для проверки работы API"""
    return Response({
        'message': 'SearchLOC API is running', 
        'status': 'OK',
        'version': '1.0'
    })

# Рестораны
class RestaurantListAPIView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cuisine_type', 'metro_station']

class RestaurantDetailAPIView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

@api_view(['GET'])
def restaurant_search(request):
    query = request.GET.get('q', '')
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurant.objects.all()
    
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response({'data': serializer.data})

# Типы кухонь
class CuisineTypeListAPIView(generics.ListAPIView):
    queryset = CuisineType.objects.all()
    serializer_class = CuisineTypeSerializer