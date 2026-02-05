from django.contrib import admin
from unfold.admin import ModelAdmin

from services.models import Service, PetType


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("name", "active", "created_at", "updated_at")
    list_filter = ("active", "created_at", "updated_at")
    search_fields = ("name", "description")
    ordering = ("name",)

@admin.register(PetType)
class PetTypeAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)