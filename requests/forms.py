from django import forms

from .models import HireRequest


class HireRequestForm(forms.ModelForm):
    caretaker_display = forms.CharField(
        label="Caretaker",
        required=False,
        disabled=True,
    )

    class Meta:
        model = HireRequest
        fields = [
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

        self.fields["client_name"].widget.attrs.setdefault("placeholder", "e.g. Alex Petrov")
        self.fields["client_email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["client_phone"].widget.attrs.setdefault("placeholder", "+359 ...")

        caretaker_widget = self.fields["caretaker_display"].widget
        caretaker_widget.attrs.setdefault("class", "form-control")
        caretaker_widget.attrs.setdefault("readonly", True)

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-control")
                continue

            if isinstance(widget, forms.DateInput):
                widget.attrs.setdefault("class", "form-control")
                continue

            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
                continue

            widget.attrs.setdefault("class", "form-control")
