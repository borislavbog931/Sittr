from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from caretakers.models import Caretaker
from services.forms import ServiceForm
from services.models import Service


class StaffOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied


def service_list(request):
    services = Service.objects.all().order_by("name")
    context = {"services": services}
    return render(request, "services/list.html", context)

class ServiceDetailView(TemplateView):
    template_name = "services/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = get_object_or_404(Service, pk=self.kwargs["pk"])
        caretakers = (
            Caretaker.objects.filter(services=service, active=True)
            .distinct()
            .order_by("name")
        )
        context["service"] = service
        context["caretakers"] = caretakers
        return context


class ServiceCreateView(StaffOnlyMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/create.html"

    def get_success_url(self):
        return reverse("service_detail", kwargs={"pk": self.object.pk})


class ServiceUpdateView(StaffOnlyMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/edit.html"

    def get_success_url(self):
        return reverse("service_detail", kwargs={"pk": self.object.pk})

class ServiceDeleteView(StaffOnlyMixin, DeleteView):
    model = Service
    template_name = "services/delete.html"

    def get_success_url(self):
        return reverse("service_list")
