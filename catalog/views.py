# catalog/views.py

from django.shortcuts import render
from .forms import ContactForm
from .models import Product
from django.http import Http404


def home(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'catalog/home.html', context)


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


def index(request):
    try:
        # Измените 'pk=1' в соответствии с вашими критериями запроса
        product = Product.objects.get(id=6)
        c = product.description.split('-')
        context = {'name': product.name, 'category': product.category, "purchase_price": product.purchase_price,
                    'description': c, 'image': product.image}
        example = {'product': product, 'split': product.description.split('-') }
        print(product)
    except Product.DoesNotExist:
        raise Http404("Продукт не существует")
    return render(request, r'catalog/index.html', example)

