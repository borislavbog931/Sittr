from django.db.models import Count, Avg
from django.shortcuts import redirect, render

from caretakers.models import Caretaker
from services.models import Service, PetType
from .translations import LANGUAGES


def home_page(request):
    featured_caretakers = (
        Caretaker.objects.filter(active=True)
        .annotate(
            avg_rating=Avg("reviews__rating"),
            reviews_count=Count("reviews", distinct=True),
        )
        .filter(reviews_count__gt=0)
        .order_by("-avg_rating", "-reviews_count")[:10]
    )
    return render(request, "common/home.html", {
        "services": Service.objects.all().order_by("name"),
        "pet_types": PetType.objects.all().order_by("name"),
        "featured_caretakers": featured_caretakers,
        "open_pet_postings": [],
    })

def about_page(request):
    return render(request, "common/about.html")

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def custom_403(request, exception):
    return render(request, "403.html", status=403)

def set_language(request, lang_code):
    if lang_code in LANGUAGES:
        request.session["language"] = lang_code
    referer = request.META.get("HTTP_REFERER")
    return redirect(referer or "home")

def coming_soon_page(request):
    return render(request, "common/coming_soon.html")

def help_page(request):
    return render(request, "common/help.html")

def pricing_page(request):
    return render(request, "common/pricing.html")

def how_it_works_sittrs_page(request):
    return render(request, "common/how_it_works_sittrs.html")

def how_it_works_owners_page(request):
    return render(request, "common/how_it_works_owners.html")

def terms_page(request):
    return render(request, "common/terms.html")

def privacy_page(request):
    return render(request, "common/privacy.html")

def cookie_policy_page(request):
    return render(request, "common/cookie_policy.html")

