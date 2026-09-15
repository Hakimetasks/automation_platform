from django.contrib import admin
from django.urls import path
from core.views import request_login, verify_login, login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_page, name='login_page'),
    path('api/auth/request-login/', request_login, name='request_login'),
    path('api/auth/verify-login/', verify_login, name='verify_login'),
]
