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
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        help_text="Выберите категорию",
        related_name="products",
    )
    price = models.DecimalField(
        blank=True,
        null=True,
        verbose_name="Цена продукта",
        help_text="Введите цену",
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("name", "category", "created_at", "updated_at", "price")

    def __str__(self):
        return self.name


class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    email = models.EmailField(verbose_name="Почта")
    phone = models.CharField(max_length=10, verbose_name="Телефон")

    def __str__(self) -> str:
        return f"{self.name} - {self.email} - {self.phone}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class ClientMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=12, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлено")
    is_answered = models.BooleanField(default=False, verbose_name="Рассмотрено")

    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["created_at"]