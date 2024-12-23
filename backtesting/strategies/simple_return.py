from .base import BaseStrategy
from portfolio.models import HistoricalStockData


class SimpleReturnStrategy(BaseStrategy):
    def run(self, stock, start_date, end_date):
        historical_data = HistoricalStockData.objects.filter(
            stock=stock, date__range=[start_date, end_date]
        ).order_by("date")

        if not historical_data.exists():
            return {"error": "No historical data available."}

        start_price = historical_data.first().close_price
        end_price = historical_data.last().close_price
        return_percentage = ((end_price - start_price) / start_price) * 100

        return {
            "strategy": "Simple Return",
            "start_date": start_date,
            "end_date": end_date,
            "return_percentage": round(return_percentage, 2),
        }
