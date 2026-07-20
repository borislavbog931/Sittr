from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from common.form_styles import BASE_INPUT


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        error_messages = {
            "username": {
                "required": "Please choose a username.",
                "unique": "That username is already taken.",
            },
            "email": {
                "required": "Please enter an email address.",
                "invalid": "Enter a valid email address.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.setdefault("placeholder", "e.g. jordan_lee")
        self.fields["email"].widget.attrs.setdefault("placeholder", "name@example.com")
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", BASE_INPUT)


class SittrAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", BASE_INPUT)
