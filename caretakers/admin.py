from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Caretaker


@admin.register(Caretaker)
class CaretakerAdmin(ModelAdmin):
    list_display = ("name", "email", "city","price_per_hour", "active", )
    list_filter = ("active", "city")
    search_fields = ("name", "email", "city")
    prepopulated_fields = {"slug": ("name", "city")}
    filter_horizontal = ("services", "pet_types")

