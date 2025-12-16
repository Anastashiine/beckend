from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer
from restaurants.models import Restaurant

# Создание отзыва
class ReviewCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Список отзывов пользователя
class UserReviewsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created_at')

# Отзывы для конкретного ресторана
class RestaurantReviewsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return Review.objects.filter(restaurant_id=restaurant_id).order_by('-created_at')

# Редактирование/удаление отзыва
class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

# Статистика ресторана
@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_stats(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        stats = Review.objects.filter(restaurant=restaurant).aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        return Response({
            'restaurant_id': restaurant_id,
            'restaurant_name': restaurant.name,
            'average_rating': round(stats['average_rating'] or 0, 2),
            'total_reviews': stats['total_reviews']
        })
    except Restaurant.DoesNotExist:
        return Response({'error': 'Ресторан не найден'}, status=status.HTTP_404_NOT_FOUND)