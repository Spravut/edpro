# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:course_id>/enroll/', views.EnrollInCourseView.as_view(), name='enroll_in_course'),
    path('course/create/', views.CourseCreateView.as_view(), name='create_course'),
    path('course/<int:course_id>/edit/', views.CourseUpdateView.as_view(), name='edit_course'),
    path('tutors/', views.TutorsView.as_view(), name='tutors'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('register/student/', views.StudentRegisterView.as_view(), name='register_student'),
    path('register/tutor/', views.TutorRegisterView.as_view(), name='register_tutor'),
    path('not-a-tutor/', views.NotATutorView.as_view(), name='not_a_tutor'),
]