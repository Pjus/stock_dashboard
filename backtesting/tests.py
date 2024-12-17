from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import CustomUser
from portfolio.models import Stock, HistoricalStockData
from backtesting.models import Backtest

class BacktestAPITestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.stock = Stock.objects.create(
            portfolio=None,
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=150.00,
            purchase_date="2024-01-01"
        )
        HistoricalStockData.objects.bulk_create([
            HistoricalStockData(stock=self.stock, date="2024-01-01", open_price=145, high_price=150, low_price=140, close_price=145, volume=100000),
            HistoricalStockData(stock=self.stock, date="2024-01-02", open_price=150, high_price=155, low_price=145, close_price=155, volume=120000),
        ])

    def test_backtest_success(self):
        data = {
            "stock_id": self.stock.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
        }
        response = self.client.post("/api/backtesting/backtest/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("return_percentage", response.data["data"])
        self.assertEqual(response.data["data"]["return_percentage"], 6.9)

    def test_backtest_missing_parameters(self):
        data = {"stock_id": self.stock.id, "start_date": "2024-01-01"}
        response = self.client.post("/api/backtesting/backtest/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)