
from django.urls import path
from .views import (
    StockEntryView,
    StockExitView,
    MovementHistoryView,
)

urlpatterns = [
    path(
        "stock-entry/",
        StockEntryView.as_view(),
        name="stock-entry",
    ),
    path(
        "stock-exit/",
        StockExitView.as_view(),
        name="stock-exit",
    ),
    path(
        "movement-history/",
        MovementHistoryView.as_view(),
        name="movement-history",
    ),
]
