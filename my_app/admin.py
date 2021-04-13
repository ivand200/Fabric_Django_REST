from django.contrib import admin

from .models import User, Survey

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Survey)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "answer", "created_at")
