from django.db import models
from portfolio.models import Stock

class Backtest(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='backtests')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='backtests')
    start_date = models.DateField()
    end_date = models.DateField()
    return_percentage = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.ticker} Backtest ({self.start_date} - {self.end_date})"