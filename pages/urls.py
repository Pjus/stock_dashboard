from django.urls import path
from . import views
from accounts.views import logout_view

urlpatterns = [
    path('', views.home, name='home'),  # 기본 페이지
    path('about/', views.about, name='about'),  # About 페이지
    path('api-docs/', views.api_docs, name='api_docs'),  # API Docs 페이지

    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('me/', views.user_detail_page, name='user_detail_page'),
    path('logout/', logout_view, name='logout_page'),

]
