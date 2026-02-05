from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models

from caretakers.models import Caretaker


class Review(models.Model):
    caretaker = models.ForeignKey(
        Caretaker,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    reviewer_name = models.CharField(
        max_length=80,
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating from 1 to 10.",
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.caretaker} - {self.rating}/10"
