from portfolio.utils import fetch_and_store_historical_data
from portfolio.models import Stock, HistoricalStockData
from portfolio.models import Stock
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import CustomUser
from .models import Portfolio, Stock


class PortfolioTestCase(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 테스트용 포트폴리오 생성
        self.portfolio = Portfolio.objects.create(
            user=self.user, name="My Portfolio", description="Test portfolio")

    def test_create_portfolio(self):
        """포트폴리오 생성 테스트"""
        data = {
            "name": "Tech Portfolio",
            "description": "A portfolio for tech stocks"
        }
        response = self.client.post('/api/portfolios/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Portfolio.objects.count(), 2)  # 기존 포트폴리오 + 새 포트폴리오
        self.assertEqual(response.data['name'], data['name'])

    def test_get_portfolios(self):
        """포트폴리오 목록 조회 테스트"""
        response = self.client.get('/api/portfolios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.portfolio.name)

    def test_update_portfolio(self):
        """포트폴리오 수정 테스트"""
        data = {
            "name": "Updated Portfolio",
            "description": "Updated description"
        }
        response = self.client.put(
            f'/api/portfolios/{self.portfolio.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.name, data['name'])
        self.assertEqual(self.portfolio.description, data['description'])

    def test_delete_portfolio(self):
        """포트폴리오 삭제 테스트"""
        response = self.client.delete(f'/api/portfolios/{self.portfolio.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Portfolio.objects.count(), 0)


class StockTestCase(TestCase):
    def setUp(self):
        # 테스트용 사용자 및 포트폴리오 생성
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.portfolio = Portfolio.objects.create(
            user=self.user, name="My Portfolio", description="Test portfolio")

        # 테스트용 종목 생성
        self.stock = Stock.objects.create(
            portfolio=self.portfolio,
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=150.00,
            purchase_date="2024-01-01"
        )

    def test_add_stock(self):
        """종목 추가 테스트"""
        data = {
            "ticker": "TSLA",
            "name": "Tesla Inc.",
            "quantity": 5,
            "purchase_price": 700.00,
            "purchase_date": "2024-02-01"
        }
        response = self.client.post(
            f'/api/portfolios/{self.portfolio.id}/stocks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 2)  # 기존 종목 + 새 종목
        self.assertEqual(response.data['ticker'], data['ticker'])

    def test_get_stocks(self):
        """종목 목록 조회 테스트"""
        response = self.client.get(
            f'/api/portfolios/{self.portfolio.id}/stocks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], self.stock.ticker)

    def test_update_stock(self):
        """종목 수정 테스트"""
        data = {
            "ticker": "AAPL",
            "name": "Apple Inc. Updated",
            "quantity": 15,
            "purchase_price": 160.00,
            "purchase_date": "2024-01-01"
        }
        response = self.client.put(
            f'/api/portfolios/{self.portfolio.id}/stocks/{self.stock.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.name, data['name'])
        self.assertEqual(self.stock.quantity, data['quantity'])

    def test_delete_stock(self):
        """종목 삭제 테스트"""
        response = self.client.delete(
            f'/api/portfolios/{self.portfolio.id}/stocks/{self.stock.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Stock.objects.count(), 0)


class UpdateStockPricesTestCase(TestCase):
    def setUp(self):
        # 테스트용 사용자 및 포트폴리오 생성
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
        self.stock1 = Stock.objects.create(
            portfolio=self.portfolio,  # 포트폴리오를 반드시 연결
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=150.00,
            purchase_date="2024-01-01",
            current_price=145.00,
        )
        self.stock2 = Stock.objects.create(
            portfolio=self.portfolio,  # 포트폴리오를 반드시 연결
            ticker="TSLA",
            name="Tesla Inc.",
            quantity=5,
            purchase_price=700.00,
            purchase_date="2024-02-01",
            current_price=720.00,
        )

    @patch("portfolio.utils.yf.Ticker")
    def test_update_all_stocks(self, mock_yf_ticker):
        """전체 주식 현재가 업데이트 테스트"""
        # Mock 데이터를 설정합니다
        mock_yf_ticker.return_value.info = {
            "regularMarketPrice": 160.00
        }

        # API 호출
        response = self.client.post("/api/portfolios/update-prices/")

        # 응답 검증
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         "Stock prices updated successfully!")

        # 데이터베이스 업데이트 검증
        self.stock1.refresh_from_db()
        self.stock2.refresh_from_db()

        self.assertEqual(self.stock1.current_price, 160.00)  # AAPL의 현재가 확인
        self.assertEqual(self.stock2.current_price, 160.00)  # TSLA의 현재가 확인

    @patch("portfolio.utils.yf.Ticker")
    def test_update_stock_error_handling(self, mock_yf_ticker):
        """특정 주식 업데이트 시 오류 발생 처리 테스트"""
        # Mock 데이터를 설정하여 오류를 발생시킵니다
        def mock_info(*args, **kwargs):
            raise Exception("Unable to fetch stock data.")
        mock_yf_ticker.return_value.info = property(mock_info)

        # API 호출
        response = self.client.post("/api/portfolios/update-prices/")

        # 응답 검증
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         "Stock prices updated successfully!")

        # 데이터베이스 확인 (가격이 변경되지 않아야 함)
        self.stock1.refresh_from_db()
        self.stock2.refresh_from_db()

        self.assertEqual(self.stock1.current_price, 145.00)  # 업데이트 실패, 기존 값 유지
        self.assertEqual(self.stock2.current_price, 720.00)  # 업데이트 실패, 기존 값 유지


class HistoricalStockDataTestCase(TestCase):
    def setUp(self):
        # 테스트용 Stock 생성
        self.stock = Stock.objects.create(
            ticker="AAPL",
            name="Apple Inc.",
            quantity=10,
            purchase_price=150.00,
            purchase_date="2024-01-01"
        )

    def test_fetch_and_store_historical_data(self):
        """히스토리컬 데이터 가져오기 및 저장 테스트"""
        fetch_and_store_historical_data(self.stock)
        historical_count = HistoricalStockData.objects.filter(
            stock=self.stock).count()
        self.assertTrue(historical_count > 0)  # 데이터가 저장되었는지 확인
