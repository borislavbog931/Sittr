from django.conf import settings
from django.db import models


class Profile(models.Model):
    OWNER = "owner"
    CARETAKER = "caretaker"
    ROLE_CHOICES = (
        (OWNER, "Owner"),
        (CARETAKER, "Caretaker"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_owner(self):
        return self.role == self.OWNER

    @property
    def is_caretaker(self):
        return self.role == self.CARETAKER
