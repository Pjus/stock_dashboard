from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # Pages 앱의 URL 연결
    path('api/accounts/', include('accounts.urls')),
    path('api/portfolios/', include('portfolio.urls')),
    path('api/backtesting/', include('backtesting.urls')),
    path('api/recommendations/', include('recommendations.urls')),
]
