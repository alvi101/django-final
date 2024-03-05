from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # implicit password field
        fields = ['username', 'first_name', 'last_name', 'email',]

    def save(self, commit=True):
        current_user = super().save(commit=False)
        if commit:
            current_user.save()
            UserAccount.objects.create(user=current_user)
        return current_user