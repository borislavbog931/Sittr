from django import forms

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

        base_input = (
            "w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm "
            "text-slate-900 placeholder:text-slate-400 focus:border-teal-400 "
            "focus:outline-none focus:ring-2 focus:ring-teal-200"
        )
        base_textarea = base_input
        base_select = (
            "w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm "
            "text-slate-900 focus:border-teal-400 focus:outline-none focus:ring-2 focus:ring-teal-200"
        )
        base_checkbox = "h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-300"
        base_file = (
            "block w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm "
            "text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-teal-50 "
            "file:px-3 file:py-2 file:text-xs file:font-semibold file:text-teal-700 "
            "hover:file:bg-teal-100"
        )
        price_input = "w-full bg-transparent p-0 text-sm text-slate-900 focus:outline-none focus:ring-0"

        # Basic placeholders (optional)
        self.fields["name"].widget.attrs.setdefault("placeholder", "e.g. Maria Ivanova")
        self.fields["city"].widget.attrs.setdefault("placeholder", "e.g. Sofia")
        self.fields["email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["phone_number"].widget.attrs.setdefault("placeholder", "+359 ...")

        for field_name, field in self.fields.items():
            widget = field.widget

            # Checkbox lists: add class to the *container* (<ul>), not the inputs
            if isinstance(widget, forms.CheckboxSelectMultiple):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = f"{existing} sittr-checklist".strip()
                continue

            # Single checkbox (active)
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", base_checkbox)
                continue

            # File input
            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", base_file)
                continue

            # Textarea
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", base_textarea)
                continue

            # Price number input (optional)
            if field_name == "price_per_hour":
                widget.attrs.setdefault("class", price_input)
                widget.attrs.setdefault("inputmode", "decimal")
                continue

            # Default
            widget.attrs.setdefault("class", base_input)
