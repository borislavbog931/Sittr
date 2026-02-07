from django.shortcuts import get_object_or_404, redirect, render

from caretakers.models import Caretaker
from .forms import HireRequestForm
from django.contrib import messages

from .models import HireRequest


def hire_request_create(request, caretaker_slug):
    caretaker = get_object_or_404(Caretaker, slug=caretaker_slug, active=True)

    if request.method == "POST":
        form = HireRequestForm(request.POST)
        if form.is_valid():
            hire_request = form.save(commit=False)
            hire_request.caretaker = caretaker
            hire_request.save()
            messages.success(request, "Request sent successfully! The caretaker will contact you soon.")
            return redirect("caretaker_detail", slug=caretaker.slug)
    else:
        form = HireRequestForm()
    form.fields['caretaker_display'].initial = f'{caretaker.name} ({caretaker.city})'

    context = {
        "caretaker": caretaker,
        "form": form,
    }
    return render(request, "requests/create.html", context)


def hire_request_list(request):
    hire_requests = (
        HireRequest.objects
        .select_related("caretaker", "pet_type", "service")
        .order_by("-id")
    )
    return render(request, "requests/list.html", {"hire_requests": hire_requests})


def hire_request_detail(request, pk):
    hire_request = get_object_or_404(
        HireRequest.objects.select_related("caretaker", "pet_type", "service"),
        pk=pk,
    )
    return render(request, "requests/detail.html", {"hire_request": hire_request})