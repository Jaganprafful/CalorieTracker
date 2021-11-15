from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.forms import ModelForm

from CalorieTracker.models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_Client = True
        user.save()
        client = Client.objects.create(user=user)
        Profile.objects.create(relatedClient=client)
        # Client.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('caloriesGoal',)


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('age', 'weight', 'height')
