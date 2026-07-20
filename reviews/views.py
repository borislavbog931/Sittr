from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from caretakers.models import Caretaker
from .forms import ReviewForm
from .models import Review


def review_list(request):
    reviews = (
        Review.objects
        .select_related("caretaker")
        .order_by("-id")
    )
    return render(request, "reviews/list.html", {"reviews": reviews})


def review_detail(request, pk):
    review = get_object_or_404(
        Review.objects.select_related("caretaker"),
        pk=pk
    )
    return render(request, "reviews/detail.html", {"review": review})

@login_required
def review_create(request, caretaker_slug):
    caretaker = get_object_or_404(Caretaker, slug=caretaker_slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
    else:
        form = ReviewForm()

    form.fields["caretaker"].initial = caretaker
    form.fields["caretaker"].disabled = True

    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.caretaker = caretaker
        review.reviewer_name = request.user.get_full_name() or request.user.username
        review.save()
        return redirect('caretaker_detail', slug=caretaker.slug)

    return render(request, "reviews/create.html", {"form": form, "caretaker": caretaker})


@login_required
def review_create_general(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer_name = request.user.get_full_name() or request.user.username
            review.save()
            return redirect("review_detail", pk=review.pk)
    else:
        form = ReviewForm()

    return render(request, "reviews/create.html", {"form": form})
