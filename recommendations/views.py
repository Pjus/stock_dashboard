from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import recommend_by_return, recommend_by_volume_spike


class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        condition = request.data.get("condition")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if condition == "return":
            min_return = request.data.get("min_return", 5.0)  # 기본값 5%
            recommendations = recommend_by_return(
                min_return, start_date, end_date)
        elif condition == "volume_spike":
            volume_threshold = request.data.get(
                "volume_threshold", 1000000)  # 기본 거래량 기준
            recommendations = recommend_by_volume_spike(
                volume_threshold, start_date, end_date)
        else:
            return Response({"error": "Invalid condition specified."}, status=400)

        return Response({"recommendations": recommendations})
