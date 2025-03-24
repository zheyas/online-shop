
from django.contrib.auth.views import LoginView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserProfileForm
from .models import CustomUser
from django.views.generic import UpdateView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject='Добро пожаловать!',
                message='Спасибо за регистрацию в нашем сервисе!',
                from_email='admin@myproject.com',
                recipient_list=[user.email],
            )
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('login')
        return render(request, self.template_name, {'form': form})

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

