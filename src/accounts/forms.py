from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from allauth.account.adapter import DefaultAccountAdapter

class CustomSignupForm(SignupForm):
    age = forms.IntegerField()
    weight = forms.IntegerField()

    class Meta:
        model = CustomUser

    def signup(self, request,user):
        user.age = self.cleaned_data['age']
        user.weight = self.cleaned_data['weight']
        user.save()
        return user