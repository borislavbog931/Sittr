from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    caretaker_display = forms.CharField(
        label="Caretaker",
        required=False,
        disabled=True,
    )

    class Meta:
        model = Review
        fields = ["reviewer_name", "rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_input = (
            "w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm "
            "text-slate-900 placeholder:text-slate-400 focus:border-teal-400 "
            "focus:outline-none focus:ring-2 focus:ring-teal-200"
        )
        base_textarea = base_input

        self.fields["reviewer_name"].widget.attrs.setdefault("placeholder", "e.g. Jordan Lee")

        caretaker_widget = self.fields["caretaker_display"].widget
        caretaker_widget.attrs.setdefault("class", base_input)
        caretaker_widget.attrs.setdefault("readonly", True)

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", base_textarea)
                continue

            if isinstance(widget, forms.NumberInput):
                widget.attrs.setdefault("class", base_input)
                widget.attrs.setdefault("inputmode", "numeric")
                continue

            widget.attrs.setdefault("class", base_input)
