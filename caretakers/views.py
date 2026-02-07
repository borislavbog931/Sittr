from django.shortcuts import render, get_object_or_404

from caretakers.models import Caretaker


def caretaker_list(request):
    caretakers = Caretaker.objects.filter(active=True).order_by('name')
    context = {'caretakers': caretakers}
    return render(request, "caretakers/list.html", context)

def caretaker_detail(request, slug):
    caretaker = get_object_or_404(Caretaker.objects.prefetch_related("reviews"), slug=slug, active=True)
    context = {'caretaker': caretaker}
    return render(request, "caretakers/detail.html", context)