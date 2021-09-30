from django.urls import reverse_lazy,reverse
from django.contrib.auth import login, authenticate
from django.views import generic
from django.views.generic import CreateView, UpdateView,View
from django.shortcuts import render,redirect,get_object_or_404,resolve_url
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import (
    get_user_model, logout as auth_logout, login
)
from .forms import UserCreateForm,ProfileForm
from .models import Profile

User = get_user_model()

def register_user(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        #Userモデル処理
        user = user_form.save(commit=False)
        user.is_staff = True
        user.save()

        #Profileモデルの処理
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        login(
            request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect('clinics:index')
    else:
        context = {
            "user_form": user_form,
            "profile_form":profile_form,
        }

    return render(request, 'registration/signup.html', context)


class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        return render(self.request,'registration/profile.html')
        


def ProfileEditView(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'registration/profile_edit.html', {'profile_form': profile_form})


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')
