
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
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        self.success_message = "Ваше сообщение было успешно отправлено!"
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = getattr(self, 'success_message', None)
        return context

class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, id=6)  # Сделайте id параметризуемым, если нужно
        context['product'] = product
        context['split'] = product.description.split('-')
        return context
