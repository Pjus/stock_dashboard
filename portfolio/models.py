from django.db import models
from django.conf import settings


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=255)  # 포트폴리오 이름
    description = models.TextField(blank=True, null=True)  # 설명
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="stocks")
    ticker = models.CharField(max_length=10)  # 주식 티커 (e.g., AAPL, TSLA)
    name = models.CharField(max_length=255)  # 주식 이름 (e.g., Apple Inc.)
    quantity = models.IntegerField(default=0)  # 보유 주식 수
    purchase_price = models.DecimalField(
        max_digits=12, decimal_places=2)  # 매수 가격
    purchase_date = models.DateField()  # 매수 날짜
    current_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True)  # 현재 주가
    last_updated = models.DateTimeField(auto_now=True)  # 데이터 마지막 업데이트 시간

    def __str__(self):
        return f"{self.name} ({self.ticker})"