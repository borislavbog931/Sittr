from django import forms

from .models import HireRequest


class HireRequestForm(forms.ModelForm):
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
