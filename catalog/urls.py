from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, product_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", product_list, name="product-list"),
    path("product/<int:pk>/", product_detail, name="product-detail"),
    path("contacts/", contacts, name="contacts"),
]
