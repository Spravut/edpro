from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('tutors/', views.tutors, name='tutors'),
    path('projects/', views.projects, name='projects'),
    path('support/', views.support, name='support'),
]