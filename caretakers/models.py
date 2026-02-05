from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg

from services.models import Service, PetType


class Caretaker(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    price_per_hour = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    active = models.BooleanField(default=True)
    services = models.ManyToManyField(
        Service,
        related_name='caretakers',
        blank=True,
    )
    pet_types = models.ManyToManyField(
        PetType,
        related_name='caretakers',
        blank=True,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    profile_pic = models.ImageField(
        upload_to = 'caretakers/',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.city}')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name", 'city']

    def __str__(self):
        return f'{self.name} - {self.city}'

    def average_rating(self):
        return self.reviews.aggregate(avg=Avg('rating'))['avg']

