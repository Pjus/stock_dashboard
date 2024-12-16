from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/portfolios/', include('portfolio.urls')),  # portfolio 앱의 URL 포함

]
