from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from catalog.models import Product, ClientMessage


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product



class ContactsView(CreateView):
    model = ClientMessage
    fields = ["name", "phone", "message"]
    template_name = "catalog/contacts_form.html"
    success_url = reverse_lazy("catalog:contacts")


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "product_image", "category", "price"]
    success_url = reverse_lazy("catalog:product-list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "description", "product_image", "category", "price"]
    success_url = reverse_lazy("catalog:product-list")