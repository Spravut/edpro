# main/models.py

from django.db import models
from django.contrib.auth.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile')
    bio = models.TextField(max_length=1000, blank=True)
    expertise = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Преподаватель)"

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StudentProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    student_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects')
    project_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Проект {self.student_name}: {self.title}"

# main/models.py

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')  # ← добавлено!
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"