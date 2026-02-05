from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Review


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("caretaker", "reviewer_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("caretaker__name", "reviewer_name")
    ordering = ("-created_at",)
