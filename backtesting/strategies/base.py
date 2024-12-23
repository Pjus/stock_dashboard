from portfolio.models import HistoricalStockData


class BaseStrategy:
    def run(self, stock, start_date, end_date):
        """
        전략 실행 메서드. 결과는 딕셔너리로 반환.
        """
        raise NotImplementedError(
            "Each strategy must implement the 'run' method.")
