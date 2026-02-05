from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text = "ex. Dog walking, Home sitting, Overnight care, etc."
    )
    description = models.TextField(
        blank=True,
        help_text = "A brief description of the service."
    )

    active = models.BooleanField(
        default=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PetType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text="ex. Dog, Cat, Rabbit, etc."
    )

    def __str__(self):
        return self.name