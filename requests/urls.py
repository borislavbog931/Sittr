from django.urls import path

from . import views

urlpatterns = [
    path("", views.hire_request_list, name="hire_request_list"),
    path('<int:pk>/', views.hire_request_detail, name="hire_request_detail"),
    path("create/<slug:caretaker_slug>/", views.hire_request_create, name="hire_request_create"),
]
