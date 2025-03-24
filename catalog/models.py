# catalog/models.py
from django.db import models
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

class Category(models.Model):  # (Ваша существующая модель Category)
    name = models.CharField(max_length=100)
    description = models.TextField(help_text='Описание категории')

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(help_text='Описание товара')
    image = models.ImageField(upload_to='photos/', verbose_name='Фотография')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Изменено на auto_now

    is_published = models.BooleanField(default=False)  # Поле статуса публикации
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")  # Добавлено поле владельца

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

def create_product_permissions():
    content_type = ContentType.objects.get_for_model(Product)

    Permission.objects.get_or_create(
        codename='can_unpublish_product',
        name='Can unpublish product',
        content_type=content_type,
    )