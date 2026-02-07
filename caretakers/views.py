from django.shortcuts import render, get_object_or_404, redirect

from caretakers.forms import CaretakerForm
from caretakers.models import Caretaker
from services.models import Service, PetType


# def caretaker_list(request):
#     caretakers = Caretaker.objects.filter(active=True).order_by('name')
#     context = {'caretakers': caretakers}
#     return render(request, "caretakers/list.html", context)

def caretaker_detail(request, slug):
    caretaker = get_object_or_404(Caretaker.objects.prefetch_related("reviews"), slug=slug, active=True)
    context = {'caretaker': caretaker}
    return render(request, "caretakers/detail.html", context)


def caretaker_list(request):
    caretakers = Caretaker.objects.filter(active=True)

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
    }
    return render(request, "caretakers/list.html", context)

def caretaker_create(request):
    if request.method == "POST":
        form = CaretakerForm(request.POST, request.FILES)
        if form.is_valid():
            caretaker = form.save()
            return redirect('caretaker_detail', slug = caretaker.slug)
    else:
        form = CaretakerForm()
    return render(request, 'caretakers/create.html', {'form': form})

def caretaker_edit(request, slug):
    caretaker = get_object_or_404(Caretaker, slug=slug)
    if request.method == "POST":
        form = CaretakerForm(request.POST, request.FILES, instance=caretaker)
        if form.is_valid():
            caretaker = form.save()
            return redirect('caretaker_detail', slug=caretaker.slug)
    else:
        form = CaretakerForm(instance=caretaker)
    context = {'caretaker': caretaker, 'form': form}
    return render(request, 'caretakers/edit.html', {'form': form, 'caretaker': caretaker})

def caretaker_delete(request, slug):
    caretaker = get_object_or_404(Caretaker, slug=slug)
    if request.method == "POST":
        caretaker.delete()
        return redirect('caretaker_list')
    context = {'caretaker': caretaker}
    return render(request, 'caretakers/delete.html', context)