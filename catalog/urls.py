from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ContactsView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductsByCategoryView,
    ProductUnpublishView,
    ProductUpdateView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("category/<int:category_id>/", ProductsByCategoryView.as_view(), name="products-by-category"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("product/create/", ProductCreateView.as_view(), name="product-create"),
    path(
        "product/<int:pk>/update/", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"
    ),
    path(
        "product/<int:pk>/unpublish/",
        ProductUnpublishView.as_view(),
        name="product-unpublish",
    ),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]
