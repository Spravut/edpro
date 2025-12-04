from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tutor, Course, StudentProject


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    fields = ('title', 'price', 'level', 'is_free', 'created_at')
    readonly_fields = ('created_at',)


class StudentProjectInline(admin.TabularInline):
    model = StudentProject
    extra = 0
    fields = ('title', 'student_name', 'project_link')


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'expertise')
    list_filter = ('expertise',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'expertise')
    inlines = [CourseInline]

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Имя преподавателя'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor_full_name', 'price', 'level', 'is_free', 'created_at')
    list_filter = ('level', 'is_free', 'created_at')
    search_fields = ('title', 'description', 'tutor__user__username')
    inlines = [StudentProjectInline]

    def tutor_full_name(self, obj):
        return obj.tutor.user.get_full_name() or obj.tutor.user.username
    tutor_full_name.short_description = 'Преподаватель'


@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student_name', 'course_title', 'project_link')
    list_filter = ('course',)
    search_fields = ('title', 'student_name', 'description')

    def course_title(self, obj):
        return obj.course.title
    course_title.short_description = 'Курс'


class TutorInline(admin.StackedInline):
    model = Tutor
    can_delete = False
    verbose_name_plural = 'Профиль преподавателя'


class UserAdmin(BaseUserAdmin):
    inlines = (TutorInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)