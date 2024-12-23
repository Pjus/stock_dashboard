from django.urls import path
from .views import BacktestView, RunBacktestStrategyView

urlpatterns = [
    path('backtest/', BacktestView.as_view(), name='backtest'),
    path('run-strategy/', RunBacktestStrategyView.as_view(), name='run-strategy'),

]
