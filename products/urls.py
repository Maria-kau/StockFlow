from django.urls import path

from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductTrashListView,
    ProductRestoreView,
)

urlpatterns = [
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),
    path(
        "products/trash/",
        ProductTrashListView.as_view(),
        name="product-trash-list",
    ),
    path(
        "products/<int:pk>/restore/",
        ProductRestoreView.as_view(),
        name="product-restore",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]
#   \[
#       \text{path}(\text{caminho},\ \text{view},\ \text{nome})
#   \]