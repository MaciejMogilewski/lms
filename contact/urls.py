from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('form', views.ContactView.as_view(), name='form'),
]
