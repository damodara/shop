from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views import View

from catalog.forms import ProductForm
from catalog.models import ClientMessage, Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        # Для неавторизованных пользователей показываем только опубликованные
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        # Для авторизованных показываем все продукты
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


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
        return super().form_valid(form)


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


class ProductUnpublishView(LoginRequiredMixin, View):
    """View для отмены публикации продукта (только для модераторов)"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        # Проверяем право can_unpublish_product
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("У вас нет прав для отмены публикации продукта")
        
        product.is_published = False
        product.save()
        
        return redirect(reverse("catalog:product-detail", kwargs={"pk": pk}))
