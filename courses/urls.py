from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CoursesView.as_view(), name='courses'),
    path('<int:pk>/', views.CoruseDetailView.as_view(), name='course-detail'),
    path('create/', views.CreateCourseView.as_view(), name='course-create'),
    path('delete/<slug:slug>/', views.CourseDeleteView.as_view(), name='course-delete'),
    path('edit/<slug:slug>/', views.CourseUpdateView.as_view(), name='course-update'),
    path('<int:pk>/module/', views.CourseModuleUpdateView.as_view(), name='course-modules-update')
]
