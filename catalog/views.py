from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')


def contact(request):
    return render(request, 'catalog/contacts.html')

