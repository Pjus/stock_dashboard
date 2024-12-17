from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from portfolio.models import Stock
from .models import Backtest
from .utils import calculate_backtest

class BacktestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stock_id = request.data.get("stock_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not stock_id or not start_date or not end_date:
            return Response({"error": "Missing required parameters."}, status=400)

        try:
            stock = Stock.objects.get(id=stock_id, portfolio__user=request.user)
            result = calculate_backtest(stock, start_date, end_date)

            if "error" in result:
                return Response({"error": result["error"]}, status=400)

            backtest = Backtest.objects.create(
                user=request.user,
                stock=stock,
                start_date=start_date,
                end_date=end_date,
                return_percentage=result["return_percentage"]
            )

            return Response({
                "message": "Backtest successful.",
                "data": {
                    "stock": result["stock"],
                    "start_date": result["start_date"],
                    "end_date": result["end_date"],
                    "return_percentage": result["return_percentage"],
                    "backtest_id": backtest.id
                }
            })
        except Stock.DoesNotExist:
            return Response({"error": "Stock not found or not owned by the user."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)