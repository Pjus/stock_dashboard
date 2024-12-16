from .utils import fetch_and_store_historical_data
from .utils import update_all_stocks
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Stock
from .serializers import PortfolioSerializer, PortfolioCreateSerializer, StockSerializer

# 포트폴리오 리스트 및 생성


class PortfolioListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)  # 사용자 데이터 필터링

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PortfolioCreateSerializer
        return PortfolioSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 사용자 연결

# 포트폴리오 상세, 수정, 삭제


class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

# 주식 추가, 수정, 삭제


class StockListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def get_queryset(self):
        portfolio_id = self.kwargs['portfolio_id']
        return Stock.objects.filter(portfolio__id=portfolio_id, portfolio__user=self.request.user)

    def perform_create(self, serializer):
        portfolio = Portfolio.objects.get(
            id=self.kwargs['portfolio_id'], user=self.request.user)
        serializer.save(portfolio=portfolio)


class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(portfolio__user=self.request.user)


class UpdateStockPricesView(APIView):
    """
    데이터베이스에 저장된 모든 주식의 현재가를 업데이트합니다.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        update_all_stocks()
        return Response({"message": "Stock prices updated successfully!"})


class UpdateHistoricalDataView(APIView):
    """
    특정 주식의 히스토리컬 데이터를 업데이트합니다.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, stock_id):
        try:
            stock = Stock.objects.get(
                id=stock_id, portfolio__user=request.user)
            fetch_and_store_historical_data(stock)
            return Response({"message": f"Historical data for {stock.ticker} updated successfully."})
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found or not owned by the user."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
