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

        self.fields["client_name"].widget.attrs.setdefault("placeholder", "e.g. Alex Petrov")
        self.fields["client_email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["client_phone"].widget.attrs.setdefault("placeholder", "+359 ...")

        caretaker_widget = self.fields["caretaker_display"].widget
        caretaker_widget.attrs.setdefault("class", base_input)
        caretaker_widget.attrs.setdefault("readonly", True)

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", base_textarea)
                continue

            if isinstance(widget, forms.DateInput):
                widget.attrs.setdefault("class", base_input)
                continue

            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", base_select)
                continue

            widget.attrs.setdefault("class", base_input)
