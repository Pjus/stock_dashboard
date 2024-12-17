from portfolio.models import HistoricalStockData

def calculate_backtest(stock, start_date, end_date):
    historical_data = HistoricalStockData.objects.filter(
        stock=stock,
        date__range=[start_date, end_date]
    ).order_by('date')

    if not historical_data.exists():
        return {"error": "No historical data available for the given period."}

    start_price = historical_data.first().close_price
    end_price = historical_data.last().close_price
    return_percentage = ((end_price - start_price) / start_price) * 100

    return {
        "stock": stock.ticker,
        "start_date": start_date,
        "end_date": end_date,
        "return_percentage": return_percentage,
    }