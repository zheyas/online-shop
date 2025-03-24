# catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, FormView
from .models import Product
from .forms import ContactForm, ProductForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Импортируем миксины
from django.contrib.auth.decorators import login_required

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

    def get_queryset(self):
        """Отображаем продукты текущего пользователя"""
        return Product.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):  # Добавляем LoginRequiredMixin
    """Создание продукта"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Автоматическое назначение владельца
        messages.success(self.request, "Продукт успешно создан.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при создании продукта. Пожалуйста, проверьте форму на наличие ошибок.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание продукта'  # Example: For header in template
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        """Проверка, является ли пользователь владельцем"""
        obj = self.get_object()
        return obj.owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование продукта'  # Example: For header in template
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def test_func(self):
        """Проверка, является ли пользователь владельцем или модератором"""
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm('catalog.can_unpublish_product')  # Добавлена проверка на права модератора

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Продукт успешно удалён.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'  # Example: For header in template
        return context

@login_required
def toggle_publish(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка разрешения на снятие с публикации
    if request.user.has_perm('catalog.can_unpublish_product'):
        product.is_published = not product.is_published
        product.save()
        messages.success(request, f"Статус публикации продукта '{product.name}' изменен.")
    else:
        messages.error(request, "У вас нет прав на изменение статуса публикации продукта.")

    return redirect('product_list')  # Или куда нужно перенаправить