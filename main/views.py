# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Course, Tutor, StudentProject
from .forms import TutorRegistrationForm, CourseForm

def home(request):
    tutors = Tutor.objects.all()[:3]
    projects = StudentProject.objects.all()[:3]
    context = {'tutors': tutors, 'projects': projects}
    return render(request, 'main/home.html', context)

def courses(request):
    courses_list = Course.objects.all()
    return render(request, 'main/courses.html', {'courses': courses_list})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'main/course_detail.html', {'course': course})

def tutors(request):
    tutors_list = Tutor.objects.all()
    return render(request, 'main/tutors.html', {'tutors': tutors_list})

def projects(request):
    projects_list = StudentProject.objects.all()
    return render(request, 'main/projects.html', {'projects': projects_list})

def support(request):
    return render(request, 'main/support.html')

def register_tutor(request):
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = TutorRegistrationForm()
    return render(request, 'main/register_tutor.html', {'form': form})

@login_required
def create_course(request):
    if not hasattr(request.user, 'tutor_profile'):
        return render(request, 'main/not_a_tutor.html')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.tutor = request.user.tutor_profile
            course.save()
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'main/create_course.html', {'form': form})