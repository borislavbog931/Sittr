from django.db.models import Count, Avg
from django.shortcuts import redirect, render

from caretakers.models import Caretaker
from services.models import Service, PetType
from .translations import LANGUAGES


def get_pricing_snapshot():
    """Real average hourly rates from active Sittrs, overall and per pet type."""
    active_caretakers = Caretaker.objects.filter(active=True)

    overall_avg = active_caretakers.aggregate(avg=Avg("price_per_hour"))["avg"]

    by_pet_type = {}
    for pet_type in PetType.objects.all():
        avg = (
            active_caretakers.filter(pet_types=pet_type)
            .aggregate(avg=Avg("price_per_hour"))["avg"]
        )
        if avg is not None:
            by_pet_type[str(pet_type.id)] = round(float(avg), 2)

    return {
        "overall": round(float(overall_avg), 2) if overall_avg is not None else None,
        "by_pet_type": by_pet_type,
    }


def get_full_pricing_data():
    """Full calculator dataset: real per-Sittr rates plus average rates by
    pet type and by service, for when no specific Sittr is chosen."""
    active_caretakers = Caretaker.objects.filter(active=True)

    caretakers = {
        str(c.id): {"name": c.name, "rate": float(c.price_per_hour)}
        for c in active_caretakers
    }

    by_pet_type = {}
    for pet_type in PetType.objects.all():
        avg = (
            active_caretakers.filter(pet_types=pet_type)
            .aggregate(avg=Avg("price_per_hour"))["avg"]
        )
        if avg is not None:
            by_pet_type[str(pet_type.id)] = round(float(avg), 2)

    by_service = {}
    for service in Service.objects.all():
        avg = (
            active_caretakers.filter(services=service)
            .aggregate(avg=Avg("price_per_hour"))["avg"]
        )
        if avg is not None:
            by_service[str(service.id)] = round(float(avg), 2)

    overall_avg = active_caretakers.aggregate(avg=Avg("price_per_hour"))["avg"]

    return {
        "caretakers": caretakers,
        "by_pet_type": by_pet_type,
        "by_service": by_service,
        "overall": round(float(overall_avg), 2) if overall_avg is not None else None,
    }


def get_home_pet_type_choices():
    """Curated 5-option pet-type list for the home page: Dog/Cat/Bird/Fish,
    with the remaining granular small-pet types (Rabbit, Hamster, Guinea Pig,
    Reptile) merged into a single 'Small pets' option."""
    def first_match(*names):
        for name in names:
            pet_type = PetType.objects.filter(name__iexact=name).first()
            if pet_type:
                return pet_type
        return None

    candidates = [
        (first_match("Dog"), "Dog"),
        (first_match("Cat"), "Cat"),
        (first_match("Bird"), "Bird"),
        (first_match("Fish"), "Fish"),
        (first_match("Rabbit", "Hamster", "Guinea Pig", "Reptile"), "Small pets"),
    ]
    return [{"id": pet_type.id, "name": label} for pet_type, label in candidates if pet_type]


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
    dog_pet_type = PetType.objects.filter(name__iexact="Dog").first()
    cat_pet_type = PetType.objects.filter(name__iexact="Cat").first()

    return render(request, "common/home.html", {
        "services": Service.objects.all().order_by("name"),
        "pet_types": get_home_pet_type_choices(),
        "featured_caretakers": featured_caretakers,
        "open_pet_postings": [],
        "dog_pet_type": dog_pet_type,
        "cat_pet_type": cat_pet_type,
        "pricing_data_json": get_pricing_snapshot(),
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
    return render(request, "common/pricing.html", {
        "pet_types": PetType.objects.all().order_by("name"),
        "pricing_data_json": get_pricing_snapshot(),
    })

def calculator_page(request):
    return render(request, "common/calculator.html", {
        "caretakers": Caretaker.objects.filter(active=True).order_by("name"),
        "pet_types": PetType.objects.all().order_by("name"),
        "services": Service.objects.filter(active=True).order_by("name"),
        "pricing_data_json": get_full_pricing_data(),
    })

def how_it_works_sittrs_page(request):
    return render(request, "common/how_it_works_sittrs.html", {
        "pricing_data_json": get_pricing_snapshot(),
    })

def how_it_works_owners_page(request):
    return render(request, "common/how_it_works_owners.html")

def terms_page(request):
    return render(request, "common/terms.html")

def privacy_page(request):
    return render(request, "common/privacy.html")

def cookie_policy_page(request):
    return render(request, "common/cookie_policy.html")

