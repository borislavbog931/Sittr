from django import forms
from caretakers.models import Caretaker
from common.form_styles import BASE_INPUT, BASE_SELECT, BASE_TEXTAREA
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["caretaker", "reviewer_name", "rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["caretaker"].queryset = Caretaker.objects.filter(active=True).order_by("name", "city")
        self.fields["reviewer_name"].widget.attrs.setdefault("placeholder", "e.g. Jordan Lee")

        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", BASE_TEXTAREA)
                continue

            if isinstance(widget, forms.NumberInput):
                widget.attrs.setdefault("class", BASE_INPUT)
                widget.attrs.setdefault("inputmode", "numeric")
                continue

            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", BASE_SELECT)
                continue

            widget.attrs.setdefault("class", BASE_INPUT)

