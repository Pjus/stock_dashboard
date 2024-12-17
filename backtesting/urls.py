from django.urls import path
from .views import BacktestView

urlpatterns = [
    path('backtest/', BacktestView.as_view(), name='backtest'),
]