from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Adds products to database"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(
            name="Ягоды", description="Описание ягод"
        )
        products = [
            {
                "name": "Малина",
                "description": "Описание малины",
                "product_image": "",
                "category": category,
                "price": "135.00",
            },
            {
                "name": "Клубника",
                "description": "Описание клубники",
                "product_image": "",
                "category": category,
                "price": "155.00",
            },
        ]

        for product_data in products:
            product = Product.objects.create(**product_data)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added product: {product.name}")
            )
