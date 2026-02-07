from django.shortcuts import render, get_object_or_404, redirect

from services.forms import ServiceForm
from services.models import Service


def service_list(request):
    services = Service.objects.all().order_by("name")
    context = {"services": services}
    return render(request, "services/list.html", context)

def service_detail(request,pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "services/detail.html", {"service": service})


def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            return redirect("service_detail", pk=service.pk)
    else:
        form = ServiceForm()
    return render(request, "services/create.html", {"form": form})


def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            return redirect("service_detail", pk=service.pk)
        else:
            form = ServiceForm(instance=service)
        context = {"form": form, "service": service}
        return render(request, "services/edit.html", context)

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        service.delete()
        return redirect("service_list")
    return render(request, 'services/delete.html', {"service": service})