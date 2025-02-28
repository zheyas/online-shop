from django.urls import path
from .views import HomeView, ContactView, IndexView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('index/', IndexView.as_view(), name='index'),
]
