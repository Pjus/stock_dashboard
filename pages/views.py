from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')


def about(request):
    return render(request, 'pages/about.html')


def api_docs(request):
    return render(request, 'pages/api_docs.html')


def register_page(request):
    return render(request, 'accounts/register.html')


def login_page(request):
    return render(request, 'accounts/login.html')


def user_detail_page(request):
    return render(request, 'accounts/user_detail.html')
