from .strategies.simple_return import SimpleReturnStrategy
from .strategies.moving_average import MovingAverageStrategy


class StrategyRunner:
    def __init__(self):
        self.strategies = {
            "simple_return": SimpleReturnStrategy(),
            "moving_average": MovingAverageStrategy(),
        }

    def run_strategy(self, strategy_name, stock, start_date, end_date):
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Strategy '{strategy_name}' not found.")
        return strategy.run(stock, start_date, end_date)
