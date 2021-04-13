from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import UserProfile

User = get_user_model()


class UserCreateForm(UserCreationForm): 

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',)
        else:
            fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("birthday","gender","address","carrer")