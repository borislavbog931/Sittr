from django.shortcuts import get_object_or_404, redirect, render

from caretakers.models import Caretaker
from .forms import HireRequestForm
from django.contrib import messages

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

    context = {
        "caretaker": caretaker,
        "form": form,
    }
    return render(request, "requests/create.html", context)
