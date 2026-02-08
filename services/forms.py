from django import forms
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

        base_input = (
            "w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm "
            "text-slate-900 placeholder:text-slate-400 focus:border-teal-400 "
            "focus:outline-none focus:ring-2 focus:ring-teal-200"
        )
        base_textarea = base_input
        base_checkbox = "h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-300"

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", base_textarea)
                continue

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", base_checkbox)
                continue

            widget.attrs.setdefault("class", base_input)

