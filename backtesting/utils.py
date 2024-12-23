from portfolio.models import HistoricalStockData


def calculate_backtest(stock, start_date, end_date):
    """
    주어진 기간 동안 백테스팅 수익률을 계산합니다.
    """
    historical_data = HistoricalStockData.objects.filter(
        stock=stock,
        date__range=[start_date, end_date]
    ).order_by('date')

    if not historical_data.exists():
        raise ValueError("No historical data available for the given period.")

    start_price = historical_data.first().close_price
    end_price = historical_data.last().close_price

    if start_price is None or end_price is None:
        raise ValueError("Missing price data for the given period.")

    return_percentage = ((end_price - start_price) / start_price) * 100

    return {
        "stock": stock.ticker,
        "start_date": start_date,
        "end_date": end_date,
        "return_percentage": float(round(return_percentage, 2)),  # float로 변환
    }
