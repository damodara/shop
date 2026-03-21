import os

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "product_image", "category", "price", "is_published"]
        exclude = ["owner", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        
        # Показываем поле is_published только владельцу продукта
        if self.instance and self.instance.pk:
            # Редактирование существующего продукта
            if not (self.user and self.instance.owner == self.user):
                # Если пользователь не владелец, скрываем поле is_published
                self.fields.pop("is_published", None)
        else:
            # Создание нового продукта - скрываем is_published (по умолчанию False)
            self.fields.pop("is_published", None)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f"Название не может содержать слово '{word}'."
                    )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            description_lower = description.lower()
            for word in self.FORBIDDEN_WORDS:
                if word in description_lower:
                    raise ValidationError(
                        f"Описание не может содержать слово '{word}'."
                    )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_product_image(self):
        image = self.cleaned_data.get("product_image")

        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")
            valid_types = ["image/jpeg", "image/png"]
            if hasattr(image, "content_type") and image.content_type not in valid_types:
                raise ValidationError("Изображение должно быть в формате JPEG или PNG.")
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png"]:
                raise ValidationError("Разрешены только форматы .jpg, .jpeg, .png.")
        return image

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
