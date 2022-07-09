from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import models


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Provide secret password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Daj mi to hasło"
        })
    )

    password_confirmation = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Ponów hasło"
        })
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email", "password", "is_superuser")

    def clean_login(self):
        login = self.cleaned_data.get("login", None)

        if login is not None and len(login) <= 3:
            raise ValidationError("Something is no yes!")

        return login

    def clean_password(self):
        special_signs = "!@#$%^&*"
        password = self.cleaned_data.get('password', None)

        counter = 0
        for letter in password:
            if special_signs.count(letter):
                counter += 1

        if counter == 0:
            raise ValidationError("Special signs are required, my friend!")

        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password', None)
        password_confirmation = self.cleaned_data.get('password_confirmation', None)

        if password is not None and password_confirmation is not None and password != password_confirmation:
            raise ValidationError("Password don't match")

        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.is_staff = True

        if commit:
            user.save()

        return user
