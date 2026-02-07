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