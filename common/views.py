from django.db.models import Count, Avg
from django.shortcuts import render

from caretakers.models import Caretaker
from services.models import Service, PetType


def home_page(request):
    featured_caretakers = (
        Caretaker.objects.filter(active=True)
        .annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True),
        )
        .filter(reviews_count__gt=0)
        .order_by("-avg_rating", "-reviews_count")[:3]
    )
    return render(request, "common/home.html", {
        "services": Service.objects.all().order_by("name"),
        "pet_types": PetType.objects.all().order_by("name"),
        "featured_caretakers": featured_caretakers,
    })

def about_page(request):
    return render(request, "common/about.html")

def custom_404(request, exception):
    return render(request, "404.html", status=404)

