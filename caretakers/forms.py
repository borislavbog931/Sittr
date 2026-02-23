from django import forms

from common.form_styles import (
    BASE_CHECKBOX,
    BASE_FILE,
    BASE_INPUT,
    BASE_TEXTAREA,
    PRICE_INPUT,
)
from caretakers.models import Caretaker


class CaretakerForm(forms.ModelForm):
    class Meta:
        model = Caretaker
        fields=[
            'name',
            'email',
            'phone_number',
            'city',
            'bio',
            'price_per_hour',
            'services',
            'pet_types',
            'profile_pic',
            'active',
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            'services': forms.CheckboxSelectMultiple(),
            'pet_types': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.setdefault("placeholder", "e.g. Maria Ivanova")
        self.fields["city"].widget.attrs.setdefault("placeholder", "e.g. Sofia")
        self.fields["email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["phone_number"].widget.attrs.setdefault("placeholder", "+359 ...")

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxSelectMultiple):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{existing} sittr-checklist".strip()
                continue

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", BASE_CHECKBOX)
                continue

            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", BASE_FILE)
                continue

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", BASE_TEXTAREA)
                continue

            if field_name == "price_per_hour":
                widget.attrs.setdefault("class", PRICE_INPUT)
                widget.attrs.setdefault("inputmode", "decimal")
                continue

            widget.attrs.setdefault("class", BASE_INPUT)

