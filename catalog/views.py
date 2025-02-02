# catalog/views.py

from django.shortcuts import render
from .forms import ContactForm


def home(request):
    return render(request, 'catalog/home.html')


def contact(request):
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']

            # Например, вы можете здесь вызывать отправку email или сохранять в базу данных

            # Установите сообщение об успешной отправке
            success_message = "Ваше сообщение было успешно отправлено!"
            form = ContactForm()  # Очистите форму для нового ввода
    else:
        form = ContactForm()

    return render(request, 'catalog/contacts.html', {'form': form, 'success_message': success_message})
