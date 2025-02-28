from django.views.generic import ListView, FormView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Product
from .forms import ContactForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # Изменено для соответствия шаблону


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = '/contacts/'

    def form_valid(self, form):
        # name = form.cleaned_data['name']
        # message = form.cleaned_data['message']

        # Примерный код для использования данных (например, отправка email)

        # Устанавливаем success_message для отображения в шаблоне
        self.success_message = "Ваше сообщение было успешно отправлено!"

        # Вызываем стандартное поведение form_valid
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = getattr(self, 'success_message', None)
        return context


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, id=6)
        context['product'] = product
        context['split'] = product.description.split('-')
        return context
