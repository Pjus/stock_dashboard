import yfinance as yf
from .models import Stock


def update_stock_price(ticker):
    """
    yfinance로 특정 티커의 데이터를 가져와 현재가를 반환합니다.
    """
    try:
        stock_data = yf.Ticker(ticker)
        current_price = stock_data.info.get('regularMarketPrice', None)
        return current_price
    except Exception as e:
        print(f"Error fetching data for ticker {ticker}: {e}")
        return None


def update_all_stocks():
    """
    데이터베이스에 저장된 모든 주식의 현재가를 업데이트합니다.
    """
    stocks = Stock.objects.all()
    for stock in stocks:
        current_price = update_stock_price(stock.ticker)
        if current_price is not None:
            stock.current_price = current_price
            stock.save()
            print(f"Updated {stock.ticker}: {current_price}")
