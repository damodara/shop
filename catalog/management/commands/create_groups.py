from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product
from blog.models import BlogPost


class Command(BaseCommand):
    help = "Создает группы Модератор продуктов и Контент-менеджер с необходимыми разрешениями"

    def handle(self, *args, **options):
        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # Получаем разрешения для Product
        delete_permission = Permission.objects.get(
            codename="delete_product",
            content_type=product_content_type,
        )
        can_unpublish_permission = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=product_content_type,
        )

        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        # Добавляем разрешения группе "Модератор продуктов"
        moderator_group.permissions.add(delete_permission, can_unpublish_permission)
        self.stdout.write(
            self.style.SUCCESS(
                'Разрешения добавлены группе "Модератор продуктов": '
                'delete_product, can_unpublish_product'
            )
        )

        # Создаем группу "Контент-менеджер" для блога
        blog_content_type = ContentType.objects.get_for_model(BlogPost)
        
        # Получаем все разрешения для BlogPost
        blog_permissions = Permission.objects.filter(content_type=blog_content_type)
        
        content_manager_group, created = Group.objects.get_or_create(name="Контент-менеджер")
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Контент-менеджер" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Контент-менеджер" уже существует')
            )

        # Добавляем все разрешения для блога группе "Контент-менеджер"
        content_manager_group.permissions.set(blog_permissions)
        self.stdout.write(
            self.style.SUCCESS(
                f'Разрешения для блога добавлены группе "Контент-менеджер" '
                f'({blog_permissions.count()} разрешений)'
            )
        )

        self.stdout.write(
            self.style.SUCCESS("\nГруппы успешно созданы и настроены!")
        )
