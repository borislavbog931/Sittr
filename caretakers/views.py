from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from caretakers.forms import CaretakerForm
from caretakers.models import Caretaker
from services.models import Service, PetType


# def caretaker_list(request):
#     caretakers = Caretaker.objects.filter(active=True).order_by('name')
#     context = {'caretakers': caretakers}
#     return render(request, "caretakers/list.html", context)

def caretaker_detail(request, slug):
    caretaker = get_object_or_404(
        Caretaker.objects.filter(active=True)
        .prefetch_related("reviews", "services", "pet_types"),
        slug=slug,
    )
    context = {'caretaker': caretaker}
    return render(request, "caretakers/detail.html", context)


def caretaker_list(request):
    caretakers = (
        Caretaker.objects.filter(active=True)
        .prefetch_related("services", "pet_types", "reviews")
    )

    city = (request.GET.get("city") or "").strip()
    service_id = request.GET.get("service") or ""
    pet_type_id = request.GET.get("pet_type") or ""
    max_price = request.GET.get("max_price") or ""

    if city:
        caretakers = caretakers.filter(city__icontains=city)

    if service_id:
        caretakers = caretakers.filter(services__id=service_id)

    if pet_type_id:
        caretakers = caretakers.filter(pet_types__id=pet_type_id)

    if max_price:
        try:
            caretakers = caretakers.filter(price_per_hour__lte=max_price)
        except (ValueError, TypeError):
            max_price = ""

    caretakers = caretakers.distinct().order_by("name", "city")

    markers = [
        {
            "id": caretaker.id,
            "name": caretaker.name,
            "city": caretaker.city,
            "lat": caretaker.latitude,
            "lng": caretaker.longitude,
            "price": str(caretaker.price_per_hour),
            "detail_url": reverse("caretaker_detail", args=[caretaker.slug]),
        }
        for caretaker in caretakers
        if caretaker.latitude is not None and caretaker.longitude is not None
    ]

    context = {
        "caretakers": caretakers,
        "services": Service.objects.filter(active=True).order_by("name"),
        "pet_types": PetType.objects.all().order_by("name"),
        "filters": {
            "city": city,
            "service": service_id,
            "pet_type": pet_type_id,
            "max_price": max_price,
        },
        "markers": markers,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, "caretakers/list.html", context)

@login_required
def caretaker_create(request):
    existing = getattr(request.user, "caretaker_profile", None)
    if existing:
        messages.info(request, "You already have a caretaker profile.")
        return redirect("caretaker_edit", slug=existing.slug)

    profile = getattr(request.user, "profile", None)
    if profile and not profile.is_caretaker:
        messages.error(request, "Only caretaker accounts can create a caretaker profile.")
        return redirect("home")

    if request.method == "POST":
        form = CaretakerForm(request.POST, request.FILES)
        if form.is_valid():
            caretaker = form.save(commit=False)
            caretaker.user = request.user
            caretaker.save()
            form.save_m2m()
            messages.success(request, "Caretaker created successfully.")
            return redirect('caretaker_detail', slug = caretaker.slug)
    else:
        form = CaretakerForm()
    return render(request, 'caretakers/create.html', {'form': form})

@login_required
def caretaker_edit(request, slug):
    caretaker = get_object_or_404(Caretaker, slug=slug)
    if caretaker.user_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        form = CaretakerForm(request.POST, request.FILES, instance=caretaker)
        if form.is_valid():
            caretaker = form.save()
            messages.success(request, "Caretaker updated successfully.")
            return redirect('caretaker_detail', slug=caretaker.slug)
    else:
        form = CaretakerForm(instance=caretaker)
    context = {'caretaker': caretaker, 'form': form}
    return render(request, 'caretakers/edit.html', {'form': form, 'caretaker': caretaker})

@login_required
def caretaker_delete(request, slug):
    caretaker = get_object_or_404(Caretaker, slug=slug)
    if caretaker.user_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        caretaker.delete()
        return redirect('caretaker_list')
    context = {'caretaker': caretaker}
    return render(request, 'caretakers/delete.html', context)
