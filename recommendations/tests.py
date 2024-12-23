from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import CustomUser
from portfolio.models import Portfolio, Stock, HistoricalStockData
from datetime import date


class RecommendationAPITest(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 테스트용 포트폴리오 생성
        self.portfolio = Portfolio.objects.create(
            user=self.user,
            name="My Portfolio",
            description="Test portfolio"
        )

        # 테스트용 주식 생성
        self.stock = Stock.objects.create(
            portfolio=self.portfolio,  # 포트폴리오 필수
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=150.00,
            purchase_date=date(2024, 1, 1),
        )

        # 테스트용 히스토리컬 데이터 생성
        HistoricalStockData.objects.bulk_create([
            HistoricalStockData(
                stock=self.stock,
                date="2024-01-01",
                open_price=140,
                high_price=155,
                low_price=132,
                close_price=150,
                volume=500000
            ),
            HistoricalStockData(
                stock=self.stock,
                date="2024-01-10",
                open_price=150,
                high_price=170,
                low_price=148,
                close_price=165,
                volume=1500000
            ),  # 거래량 급증
        ])

    def test_recommend_by_return(self):
        data = {"condition": "return", "start_date": "2024-01-01",
                "end_date": "2024-01-10", "min_return": 10}
        response = self.client.post("/api/recommendations/recommend/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["recommendations"]), 1)

    def test_recommend_by_volume_spike(self):
        data = {"condition": "volume_spike", "start_date": "2024-01-01",
                "end_date": "2024-01-10", "volume_threshold": 1000000}
        response = self.client.post("/api/recommendations/recommend/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["recommendations"]), 1)
