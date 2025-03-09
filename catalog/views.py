
from django.views.generic import ListView, FormView, TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from .models import Product
from .forms import ContactForm, ProductForm
from django.urls import reverse_lazy
from django.contrib import messages


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # Изменено для соответствия шаблону


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, "Ваше сообщение было успешно отправлено!")
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            product = Product.objects.get(id=6)
            context['product'] = product
            context['split'] = product.description.split('-') if product.description else []
        except Product.DoesNotExist:
            context['product'] = None
            context['split'] = []
        return context


class ProductListView(ListView):
    """Вывод списка продуктов"""
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ProductCreateView(CreateView):
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно создан.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании продукта. Пожалуйста, проверьте форму на наличие ошибок.")
        return self.render_to_response(self.get_context_data(form=form))


class ProductUpdateView(UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно обновлён.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении продукта. Пожалуйста, проверьте форму на наличие ошибок.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        return get_object_or_404(Product, pk=self.kwargs['pk'])


class ProductDeleteView(DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Продукт успешно удалён.")
        return super().delete(request, *args, **kwargs)
