from .base import BaseStrategy
import pandas as pd
from portfolio.models import HistoricalStockData


class MovingAverageStrategy(BaseStrategy):
    def run(self, stock, start_date, end_date):
        historical_data = HistoricalStockData.objects.filter(
            stock=stock, date__range=[start_date, end_date]
        ).order_by("date")

        if not historical_data.exists():
            return {"error": "No historical data available."}

        # 데이터프레임으로 변환
        df = pd.DataFrame.from_records(
            historical_data.values("date", "close_price"))
        df["SMA_5"] = df["close_price"].rolling(window=5).mean()
        df["SMA_20"] = df["close_price"].rolling(window=20).mean()

        # 전략: 이동평균 교차점 확인
        buy_signals = df[df["SMA_5"] > df["SMA_20"]]
        sell_signals = df[df["SMA_5"] < df["SMA_20"]]

        return {
            "strategy": "Moving Average Cross",
            "buy_signals": len(buy_signals),
            "sell_signals": len(sell_signals),
        }
