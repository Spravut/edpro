# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Tutor, StudentProject, Enrollment
from .forms import StudentRegistrationForm, TutorRegistrationForm, CourseForm

def home(request):
    tutors = Tutor.objects.all()[:3]
    projects = StudentProject.objects.all()[:3]
    context = {'tutors': tutors, 'projects': projects}
    return render(request, 'main/home.html', context)

def courses(request):
    # Показываем ВСЕ курсы — и платные, и бесплатные
    all_courses = Course.objects.all()
    
    # Определяем, какие курсы доступны (для кнопок/статусов)
    enrolled_course_ids = set()
    if request.user.is_authenticated:
        enrolled_course_ids = set(
            Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        )
    
    return render(request, 'main/courses.html', {
        'courses': all_courses,
        'enrolled_course_ids': enrolled_course_ids,
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Проверка: может ли пользователь видеть содержимое?
    can_access = False
    is_enrolled = False

    # Преподаватель всегда может
    if hasattr(request.user, 'tutor_profile') and course.tutor == request.user.tutor_profile:
        can_access = True
        is_enrolled = True
    # Бесплатный — всем
    elif course.is_free:
        can_access = True
        is_enrolled = True
    # Платный — только записанным
    elif request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        can_access = is_enrolled
    # Гости — не могут

    context = {
        'course': course,
        'can_access': can_access,
        'is_enrolled': is_enrolled,
    }

    return render(request, 'main/course_detail.html', context)

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not course.is_free:
        Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_detail', course_id=course.id)

def tutors(request):
    tutors_list = Tutor.objects.all()
    return render(request, 'main/tutors.html', {'tutors': tutors_list})

def projects(request):
    projects_list = StudentProject.objects.all()
    return render(request, 'main/projects.html', {'projects': projects_list})

def support(request):
    return render(request, 'main/support.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses')
    else:
        form = StudentRegistrationForm()
    return render(request, 'main/register_student.html', {'form': form})

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

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if not (hasattr(request.user, 'tutor_profile') and course.tutor == request.user.tutor_profile):
        return redirect('courses')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'main/edit_course.html', {'form': form, 'course': course})