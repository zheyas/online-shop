# catalog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, FormView, DetailView
from .models import Product, Category # Добавлен импорт Category
from .forms import ContactForm, ProductForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Импортируем миксины
from django.contrib.auth.decorators import login_required, permission_required
from django.core.cache import cache # Добавлен импорт cache
from .services import get_products_by_category  # Добавлен импорт services

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


class ProductListView(LoginRequiredMixin, ListView): # LoginRequiredMixin
    """Вывод списка продуктов"""
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        """Отображаем продукты текущего пользователя"""
        return Product.objects.filter(owner=self.request.user)

    # def get_context_data(self, **kwargs): # Не нужен, super() достаточно
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = self.get_queryset()
    #     return context


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
@permission_required('catalog.can_unpublish_product', raise_exception=True) # added
def toggle_publish(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверка разрешения на снятие с публикации # not needed any more
    # if request.user.has_perm('catalog.can_unpublish_product'):
    product.is_published = not product.is_published
    product.save()
    messages.success(request, f"Статус публикации продукта '{product.name}' изменен.")
    # else:
    #     messages.error(request, "У вас нет прав на изменение статуса публикации продукта.")

    return redirect('product_list')  # Или куда нужно перенаправить

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def get(self, request, *args, **kwargs):
        cache_key = f'product_detail_{self.kwargs["pk"]}'
        product = cache.get(cache_key)

        if product is None:
            product = self.get_object()
            cache.set(cache_key, product, timeout=60 * 5)  # Кешируем на 5 минут

        context = {'product': product}
        return render(request, self.template_name, context)

class ProductsByCategoryView(ListView):
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = get_object_or_404(Category, pk=category_id)
        return context
    def get(self, request, *args, **kwargs):
        category_id = self.kwargs['category_id']
        cache_key = f'products_by_category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            products = list(self.get_queryset())  # Convert to list for caching
            cache.set(cache_key, products, timeout=60 * 10)  # Кешируем на 10 минут

        context = self.get_context_data()
        context['products'] = products

        return render(request, self.template_name, context)