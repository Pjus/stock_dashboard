from .models import Stock, HistoricalStockData
import yfinance as yf


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


def fetch_and_store_historical_data(stock):
    """
    특정 주식의 히스토리컬 데이터를 가져와 저장합니다.
    """
    try:
        # yfinance로 데이터 가져오기
        stock_data = yf.Ticker(stock.ticker)
        historical = stock_data.history(period="1y")  # 최근 1년 데이터 가져오기

        for date, row in historical.iterrows():
            HistoricalStockData.objects.update_or_create(
                stock=stock,
                date=date,
                defaults={
                    "open_price": row['Open'],
                    "high_price": row['High'],
                    "low_price": row['Low'],
                    "close_price": row['Close'],
                    "volume": row['Volume'],
                }
            )
        print(f"Historical data for {stock.ticker} updated successfully.")
    except Exception as e:
        print(f"Error fetching historical data for {stock.ticker}: {e}")
