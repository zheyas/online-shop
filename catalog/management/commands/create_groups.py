from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' и назначает права."

    def handle(self, *args, **options):
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Получаем ContentType для Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем разрешение can_unpublish_product
        can_unpublish_permission, created = Permission.objects.get_or_create(
            codename="can_unpublish_product",
            content_type=content_type,
            defaults={'name': 'Can unpublish product'} #Указываем defaults при создании
        )

        # Получаем разрешение delete_product
        delete_product_permission = Permission.objects.get(
            codename="delete_product", content_type=content_type
        )

        moderator_group.permissions.add(can_unpublish_permission, delete_product_permission)
        moderator_group.save()

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены.'))