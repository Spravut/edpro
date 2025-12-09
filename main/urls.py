# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('tutors/', views.tutors, name='tutors'),
    path('projects/', views.projects, name='projects'),
    path('support/', views.support, name='support'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/tutor/', views.register_tutor, name='register_tutor'),
]