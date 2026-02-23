from django import forms
from common.form_styles import BASE_CHECKBOX, BASE_INPUT, BASE_TEXTAREA
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description",]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", BASE_TEXTAREA)
                continue

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", BASE_CHECKBOX)
                continue

            widget.attrs.setdefault("class", BASE_INPUT)


