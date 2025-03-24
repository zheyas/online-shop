from django.urls import path
from . import views  # Предполагается, что ваши CBV находятся в views.py

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
    # Другие URL-маршруты для приложения users
]