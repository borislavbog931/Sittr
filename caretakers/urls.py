from django.urls import path
from . import views

urlpatterns = [
    path("", views.caretaker_list, name="caretaker_list"),
    path('create/', views.caretaker_create, name='caretaker_create'),
    path('<slug:slug>/edit/', views.caretaker_edit, name='caretaker_edit'),
    path('<slug:slug>/delete/', views.caretaker_delete, name='caretaker_delete'),
    path("<slug:slug>/", views.caretaker_detail, name="caretaker_detail"),
]
