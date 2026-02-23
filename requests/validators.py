from django.core.exceptions import ValidationError
from django.utils import timezone


def start_date_not_past(value):
    today = timezone.localdate()
    if value < today:
        raise ValidationError("Start date cannot be in the past.")
