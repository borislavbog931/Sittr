from django.urls import path
from . import views

urlpatterns = [
    path("", views.caretaker_list, name="caretaker_list"),
    path("<slug:slug>/", views.caretaker_detail, name="caretaker_detail"),
]
