from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer

# Создание бронирования
class BookingCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Список бронирований пользователя
class UserBookingsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

# Детали бронирования
class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # Нельзя изменять завершенные бронирования
        instance = self.get_object()
        if instance.status == 'completed':
            raise serializers.ValidationError("Нельзя изменять завершенное бронирование")
        serializer.save()

# Отмена бронирования
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, pk):
    try:
        booking = Booking.objects.get(pk=pk, user=request.user)
        if booking.status == 'confirmed' or booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Бронирование отменено'})
        else:
            return Response(
                {'error': 'Невозможно отменить бронирование с текущим статусом'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Booking.DoesNotExist:
        return Response({'error': 'Бронирование не найдено'}, status=status.HTTP_404_NOT_FOUND)