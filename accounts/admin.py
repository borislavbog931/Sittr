from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")
