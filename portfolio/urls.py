from django.urls import path
from .views import (
    PortfolioListCreateView,
    PortfolioDetailView,
    StockListCreateView,
    StockDetailView,
    UpdateStockPricesView,
    UpdateHistoricalDataView,
)

urlpatterns = [
    path('', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('<int:portfolio_id>/stocks/',
         StockListCreateView.as_view(), name='stock-list-create'),
    path('<int:portfolio_id>/stocks/<int:pk>/',
         StockDetailView.as_view(), name='stock-detail'),
    path('update-prices/', UpdateStockPricesView.as_view(),
         name='update-stock-prices'),
    path('stocks/<int:stock_id>/update-historical-data/',
         UpdateHistoricalDataView.as_view(), name='update-historical-data'),

]
