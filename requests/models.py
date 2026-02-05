from django.core.validators import MinLengthValidator
from django.db import models

from caretakers.models import Caretaker
from services.models import Service, PetType


class HireRequest(models.Model):
    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = (
        (STATUS_NEW, "New"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    )

    caretaker = models.ForeignKey(
        Caretaker,
        on_delete=models.CASCADE,
        related_name="hire_requests",
    )

    client_name = models.CharField(
        max_length=80,
    )

    client_email = models.EmailField(blank=True)
    client_phone = models.CharField(max_length=20, blank=True)

    pet_type = models.ForeignKey(
        PetType,
        on_delete=models.PROTECT,
        related_name="hire_requests",
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="hire_requests",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.client_name} -> {self.caretaker} ({self.status})"
