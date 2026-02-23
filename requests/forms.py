from django import forms

from caretakers.models import Caretaker
from common.form_styles import BASE_INPUT, BASE_SELECT, BASE_TEXTAREA
from .models import HireRequest


class HireRequestForm(forms.ModelForm):

    class Meta:
        model = HireRequest
        fields = [
            "caretaker",
            "client_name",
            "client_email",
            "client_phone",
            "pet_type",
            "service",
            "start_date",
            "end_date",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["caretaker"].queryset = Caretaker.objects.filter(active=True).order_by("name", "city")
        self.fields["client_name"].widget.attrs.setdefault("placeholder", "e.g. Alex Petrov")
        self.fields["client_email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["client_phone"].widget.attrs.setdefault("placeholder", "+359 ...")

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", BASE_TEXTAREA)
                continue

            if isinstance(widget, forms.DateInput):
                widget.attrs.setdefault("class", BASE_INPUT)
                continue

            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", BASE_SELECT)
                continue

            widget.attrs.setdefault("class", BASE_INPUT)

