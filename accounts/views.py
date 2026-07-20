from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import Profile


def signup_choice(request):
    return render(request, "accounts/signup_choice.html")


def signup_owner(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=Profile.OWNER)
            login(request, user)
            messages.success(request, "Welcome! Your account is ready.")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "accounts/signup_owner.html", {"form": form})


def signup_caretaker(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=Profile.CARETAKER)
            login(request, user)
            messages.success(request, "Account created. Now set up your caretaker profile.")
            return redirect("caretaker_create")
    else:
        form = SignupForm()
    return render(request, "accounts/signup_caretaker.html", {"form": form})
