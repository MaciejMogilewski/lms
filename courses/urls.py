from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CoursesView.as_view(), name='courses'),
    path('<int:pk>/', views.CoruseDetailView.as_view(), name='course-detail'),
]
