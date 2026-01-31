from django.core.cache import cache
from django.conf import settings

from catalog.models import Product


def get_products_by_category(category_id):
    """
    Сервисная функция для получения списка продуктов по категории.
    Использует кеширование для оптимизации.
    """
    if settings.CACHE_ENABLED:
        cache_key = f"products_category_{category_id}"
        products = cache.get(cache_key)
        
        if products is None:
            products = list(Product.objects.filter(category_id=category_id, is_published=True))
            cache.set(cache_key, products, 60 * 15)  # Кешируем на 15 минут
    else:
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
    
    return products
