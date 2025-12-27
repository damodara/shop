from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/create/", ProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]
