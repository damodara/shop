from django.db import models


class Category(models.Model):
    name = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name="Название",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name="Название",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    product_image = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        help_text="Выберите категорию",
        related_name="products",
    )
    price = models.DecimalField(
        blank=True, null=True, verbose_name="Цена продукта", help_text="Введите цену"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
