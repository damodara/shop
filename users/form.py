from django.contrib.auth.forms import UserCreationForm
from django import forms

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserProfileForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "country", "avatar", "first_name", "last_name"]