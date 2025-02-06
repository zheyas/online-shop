from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add to DB'
    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Планшеты', description='Крутые классные планшеты прекрасные')

        products = [
            {'name': 'Redmi Pade', 'description': 'Latest model', 'category': category, 'purchase_price': 699.99},
            {'name': 'iPad', 'description': 'Latest model(ага)', 'category': category, 'purchase_price': 1699.99}
        ]
        for data in products:
            product, created = Product.objects.get_or_create(**data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Успешный успех в создании: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Вы не достигли успешного успеха: {product.name}'))
