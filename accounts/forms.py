from django import forms

from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "about")
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class CustomUserChangeForm(UserChangeForm):
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = CustomUser \
            .objects \
            .filter(username=username) \
            .exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("This username is already taken.", code="username is taken")
        return username

    class Meta:
        model = CustomUser
        fields = ("username", "about")
