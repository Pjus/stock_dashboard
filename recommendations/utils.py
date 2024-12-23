from portfolio.models import HistoricalStockData, Stock
from datetime import timedelta
import pandas as pd


def recommend_by_return(min_return_percentage, start_date, end_date):
    """
    수익률이 특정 기준 이상인 종목 추천
    """
    recommendations = []
    stocks = Stock.objects.all()

    for stock in stocks:
        historical_data = HistoricalStockData.objects.filter(
            stock=stock, date__range=[start_date, end_date]
        ).order_by('date')

        if not historical_data.exists():
            continue

        start_price = historical_data.first().close_price
        end_price = historical_data.last().close_price
        return_percentage = ((end_price - start_price) / start_price) * 100

        if return_percentage >= float(min_return_percentage):  # float 변환
            recommendations.append({
                "ticker": stock.ticker,
                "name": stock.name,
                "return_percentage": round(return_percentage, 2)
            })

    return recommendations


def recommend_by_volume_spike(volume_threshold, start_date, end_date):
    """
    거래량이 급증한 종목 추천
    """
    recommendations = []
    stocks = Stock.objects.all()

    for stock in stocks:
        historical_data = HistoricalStockData.objects.filter(
            stock=stock, date__range=[start_date, end_date]
        ).order_by('date')

        if not historical_data.exists():
            continue

        for data in historical_data:
            if data.volume >= int(volume_threshold):  # int 변환
                recommendations.append({
                    "ticker": stock.ticker,
                    "name": stock.name,
                    "date": data.date,
                    "volume": data.volume
                })
                break

    return recommendations
