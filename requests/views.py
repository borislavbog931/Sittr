from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from caretakers.models import Caretaker
from .forms import HireRequestForm
from django.contrib import messages

from .models import HireRequest


@login_required
def hire_request_create(request, caretaker_slug):
    caretaker = get_object_or_404(Caretaker, slug=caretaker_slug, active=True)

    if request.method == "POST":
        form = HireRequestForm(request.POST)
    else:
        form = HireRequestForm()

    form.fields["caretaker"].initial = caretaker
    form.fields["caretaker"].disabled = True

    if request.method == "POST" and form.is_valid():
        hire_request = form.save(commit=False)
        hire_request.caretaker = caretaker
        hire_request.requested_by = request.user
        hire_request.save()
        messages.success(request, "Request sent successfully! The caretaker will contact you soon.")
        return redirect("caretaker_detail", slug=caretaker.slug)

    context = {
        "caretaker": caretaker,
        "form": form,
    }
    return render(request, "requests/create.html", context)


@login_required
def hire_request_create_general(request):
    if request.method == "POST":
        form = HireRequestForm(request.POST)
        if form.is_valid():
            hire_request = form.save(commit=False)
            hire_request.requested_by = request.user
            hire_request.save()
            messages.success(request, "Request submitted successfully.")
            return redirect("hire_request_detail", pk=hire_request.pk)
    else:
        form = HireRequestForm()

    return render(request, "requests/create.html", {"form": form})


@login_required
def hire_request_list(request):
    hire_requests = (
        HireRequest.objects
        .select_related("caretaker", "pet_type", "service")
        .order_by("-id")
    )

    if not request.user.is_staff:
        profile = getattr(request.user, "profile", None)
        if profile and profile.is_caretaker:
            hire_requests = hire_requests.filter(caretaker__user=request.user)
        else:
            hire_requests = hire_requests.filter(requested_by=request.user)

    return render(request, "requests/list.html", {"hire_requests": hire_requests})


@login_required
def hire_request_detail(request, pk):
    hire_request = get_object_or_404(
        HireRequest.objects.select_related("caretaker", "pet_type", "service"),
        pk=pk,
    )

    if not request.user.is_staff:
        is_requester = hire_request.requested_by_id == request.user.id
        is_target_caretaker = hire_request.caretaker.user_id == request.user.id
        if not (is_requester or is_target_caretaker):
            raise PermissionDenied

    return render(request, "requests/detail.html", {"hire_request": hire_request})
