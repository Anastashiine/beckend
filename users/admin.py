from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Добавляем phone_number в поля для отображения
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    # Добавляем phone_number в поля для редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone_number',)}),
    )