from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description",]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

