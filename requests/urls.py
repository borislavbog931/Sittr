from django.urls import path

from . import views

urlpatterns = [
    path("create/<slug:caretaker_slug>/", views.hire_request_create, name="hire_request_create"),
]
