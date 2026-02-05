from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import HireRequest


@admin.register(HireRequest)
class HireRequestAdmin(ModelAdmin):
    list_display = ("client_name", "caretaker", "service", "pet_type", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "service", "pet_type", "created_at")
    search_fields = ("client_name", "client_email", "client_phone", "caretaker__name")
    ordering = ("-created_at",)
