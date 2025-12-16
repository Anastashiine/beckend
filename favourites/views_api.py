from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Favourite
from .serializers import FavouriteSerializer

# Добавление в избранное
class FavouriteCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Список избранного пользователя
class UserFavouritesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteSerializer

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user).order_by('-created_at')

# Удаление из избранного
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favourite(request, restaurant_id):
    try:
        favourite = Favourite.objects.get(user=request.user, restaurant_id=restaurant_id)
        favourite.delete()
        return Response({'message': 'Ресторан удален из избранного'})
    except Favourite.DoesNotExist:
        return Response({'error': 'Ресторан не найден в избранном'}, status=status.HTTP_404_NOT_FOUND)

# Проверка, есть ли ресторан в избранном
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favourite(request, restaurant_id):
    is_favourite = Favourite.objects.filter(
        user=request.user, 
        restaurant_id=restaurant_id
    ).exists()
    return Response({'is_favourite': is_favourite})