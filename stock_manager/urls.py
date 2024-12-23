from django.contrib import admin
from django.urls import path, include
from accounts.views import home  # 방금 만든 뷰를 import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 루트 URL에 대해 home 뷰 연결
    path('api/accounts/', include('accounts.urls')),
    path('api/portfolios/', include('portfolio.urls')),
    path('api/backtesting/', include('backtesting.urls')),
    path('api/recommendations/', include('recommendations.urls')),

]
