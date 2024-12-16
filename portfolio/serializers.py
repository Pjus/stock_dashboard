from rest_framework import serializers
from .models import Portfolio, Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'ticker', 'name', 'quantity',
                  'purchase_price', 'purchase_date', 'current_price']


class PortfolioSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)  # 연결된 종목 데이터 포함

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description',
                  'created_at', 'updated_at', 'stocks']


class PortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['name', 'description']
