# main/views.py

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.views.generic.edit import FormView

from .models import Course, Tutor, StudentProject, Enrollment
from .forms import StudentRegistrationForm, TutorRegistrationForm, CourseForm

class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tutors'] = Tutor.objects.all()[:3]
        context['projects'] = StudentProject.objects.all()[:3]
        return context


class CourseListView(ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            enrolled_ids = Enrollment.objects.filter(
                student=self.request.user
            ).values_list('course_id', flat=True)
            context['enrolled_course_ids'] = set(enrolled_ids)
        else:
            context['enrolled_course_ids'] = set()
        return context
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'main/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user

        can_access = False
        is_enrolled = False

        # Преподаватель — всегда может
        if hasattr(user, 'tutor_profile') and course.tutor == user.tutor_profile:
            can_access = True
            is_enrolled = True
        # Бесплатный — всем
        elif course.is_free:
            can_access = True
            is_enrolled = True
        # Платный — только записанным
        elif user.is_authenticated:
            is_enrolled = Enrollment.objects.filter(student=user, course=course).exists()
            can_access = is_enrolled

        context.update({
            'can_access': can_access,
            'is_enrolled': is_enrolled,
        })
        return context

class EnrollInCourseView(LoginRequiredMixin, View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        if not course.is_free:
            obj, created = Enrollment.objects.get_or_create(
                student=request.user,
                course=course
            )
            if created:
                messages.success(request, f"Вы записались на курс «{course.title}»!")
            else:
                messages.info(request, "Вы уже записаны на этот курс.")
        return redirect('course_detail', course_id=course.id)

    def get(self, request, course_id):
        # Разрешаем GET для удобства (или оставьте только POST)
        return self.post(request, course_id)


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'main/create_course.html'
    success_url = reverse_lazy('courses')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'tutor_profile'):
            return redirect('not_a_tutor')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tutor = self.request.user.tutor_profile
        return super().form_valid(form)
    
class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'main/edit_course.html'
    pk_url_kwarg = 'course_id'

    def dispatch(self, request, *args, **kwargs):
        course = self.get_object()
        if not (hasattr(request.user, 'tutor_profile') and course.tutor == request.user.tutor_profile):
            return redirect('courses')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course_detail', kwargs={'course_id': self.object.id})
    
class TutorsView(ListView):
    model = Tutor
    template_name = 'main/tutors.html'
    context_object_name = 'tutors'

class ProjectsView(ListView):
    model = StudentProject
    template_name = 'main/projects.html'
    context_object_name = 'projects'

class SupportView(TemplateView):
    template_name = 'main/support.html'

class StudentRegisterView(FormView):
    template_name = 'main/register_student.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('courses')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class TutorRegisterView(FormView):
    template_name = 'main/register_tutor.html'
    form_class = TutorRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class NotATutorView(TemplateView):
    template_name = 'main/not_a_tutor.html'