from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Путь для home.html
    path('contacts/', views.contact, name='contacts'),
    path('index/', views.index, name='index')
]

