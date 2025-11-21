from django.shortcuts import render, get_object_or_404
from .models import Course, Tutor, StudentProject

def home(request):
    tutors = Tutor.objects.all()[:3] # Пример: последние 3 преподавателя
    projects = StudentProject.objects.all()[:3] # Пример: последние 3 проекта
    context = {
        'tutors': tutors,
        'projects': projects,
    }
    return render(request, 'main/home.html', context)

def courses(request):
    courses_list = Course.objects.all()
    context = {
        'courses': courses_list
    }
    return render(request, 'main/courses.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Здесь можно добавить логику для отображения связанных отзывов, уроков и т.д.
    context = {
        'course': course
    }
    return render(request, 'main/course_detail.html', context)

def tutors(request):
    tutors_list = Tutor.objects.all()
    context = {
        'tutors': tutors_list
    }
    return render(request, 'main/tutors.html', context)

def projects(request):
    projects_list = StudentProject.objects.all()
    context = {
        'projects': projects_list
    }
    return render(request, 'main/projects.html', context)

def support(request):
    # Логика для формы поддержки будет добавлена позже
    return render(request, 'main/support.html')