from django.http import HttpResponse
from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]
