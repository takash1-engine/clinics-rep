from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UserCreate(CreateView):
    """ユーザー登録"""
    model = User
    form_class = UserCreateForm

    def form_valid(self, form):
        """ユーザー登録"""
        # formをテーブルに保存するかを指定するオプション（デフォルト=True）
        user = form.save(commit=True)
        # is_active<-ユーザーアカウントをアクティブにするかどうかを指定,
        # 退会処理も、is_activeをFalseにするという処理がベター。
        user.is_active = True
        user.save()

        return redirect('user_create_done')


class ProfileView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        return render(self.request,'registration/profile.html')


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')
