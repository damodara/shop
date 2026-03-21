from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views import View
from django.utils.decorators import method_decorator

from catalog.forms import ProductForm
from catalog.models import ClientMessage, Product, Category
from catalog.services import get_products_by_category


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        # Низкоуровневое кеширование для списка продуктов
        if settings.CACHE_ENABLED:
            cache_key = "products_list"
            queryset = cache.get(cache_key)
            
            if queryset is None:
                queryset = super().get_queryset()
                # Для неавторизованных пользователей показываем только опубликованные
                if not self.request.user.is_authenticated:
                    queryset = queryset.filter(is_published=True)
                # Кешируем на 15 минут
                cache.set(cache_key, queryset, 60 * 15)
        else:
            queryset = super().get_queryset()
            # Для неавторизованных пользователей показываем только опубликованные
            if not self.request.user.is_authenticated:
                queryset = queryset.filter(is_published=True)
        
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Низкоуровневое кеширование объекта продукта
        if settings.CACHE_ENABLED:
            cache_key = f"product_{obj.pk}"
            cached_obj = cache.get(cache_key)
            if cached_obj is None:
                cache.set(cache_key, obj, 60 * 15)  # Кешируем на 15 минут
            else:
                return cached_obj
        
        return obj


class ContactsView(CreateView):
    model = ClientMessage
    fields = ["name", "phone", "message"]
    template_name = "catalog/contacts_form.html"
    success_url = reverse_lazy("catalog:contacts")


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Автоматически привязываем продукт к текущему пользователю
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Инвалидируем кеш после создания продукта
        if settings.CACHE_ENABLED:
            cache.delete("products_list")
            cache.delete(f"products_category_{form.instance.category_id if form.instance.category_id else 'all'}")
        
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, что пользователь является владельцем
        if obj.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта")
        return obj

    def form_valid(self, form):
        old_category_id = self.object.category_id if self.object.category_id else None
        response = super().form_valid(form)
        
        # Инвалидируем кеш после обновления продукта
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{self.object.pk}")
            cache.delete("products_list")
            if old_category_id:
                cache.delete(f"products_category_{old_category_id}")
            if form.instance.category_id:
                cache.delete(f"products_category_{form.instance.category_id}")
        
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, что пользователь является владельцем или модератором
        is_owner = obj.owner == self.request.user
        is_moderator = self.request.user.groups.filter(name="Модератор продуктов").exists()
        
        if not (is_owner or is_moderator):
            raise PermissionDenied("У вас нет прав для удаления этого продукта")
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_id = obj.category_id if obj.category_id else None
        
        response = super().delete(request, *args, **kwargs)
        
        # Инвалидируем кеш после удаления продукта
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{obj.pk}")
            cache.delete("products_list")
            if category_id:
                cache.delete(f"products_category_{category_id}")
        
        return response


class ProductUnpublishView(LoginRequiredMixin, View):
    """View для отмены публикации продукта (только для модераторов)"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        # Проверяем право can_unpublish_product
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("У вас нет прав для отмены публикации продукта")
        
        product.is_published = False
        product.save()
        
        # Инвалидируем кеш после изменения продукта
        if settings.CACHE_ENABLED:
            cache.delete(f"product_{pk}")
            cache.delete("products_list")
            if product.category_id:
                cache.delete(f"products_category_{product.category_id}")
        
        return redirect(reverse("catalog:product-detail", kwargs={"pk": pk}))


class ProductsByCategoryView(ListView):
    """Представление для отображения продуктов по категории"""
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        
        # Используем сервисную функцию для получения продуктов
        products = get_products_by_category(category_id)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context["category"] = category
        return context
