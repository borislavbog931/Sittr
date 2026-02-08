from django.shortcuts import get_object_or_404, render, redirect

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

def review_create(request, caretaker_slug):
    caretaker = get_object_or_404(Caretaker, slug=caretaker_slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        form.fields["caretaker_display"].initial = f"{caretaker.name} ({caretaker.city})"
        if form.is_valid():
            review = form.save(commit=False)
            review.caretaker = caretaker
            review.save()
            return redirect('caretaker_detail', slug=caretaker.slug)
    else:
        form = ReviewForm()
        form.fields["caretaker_display"].initial = f"{caretaker.name} ({caretaker.city})"
    return render(request, "reviews/create.html", {"form": form, "caretaker": caretaker})
