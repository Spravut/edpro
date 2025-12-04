# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course

class TutorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    expertise = forms.CharField(max_length=200, label="Область экспертизы (например: Python, Математика)")
    bio = forms.CharField(widget=forms.Textarea, label="Краткая биография", required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            from .models import Tutor
            Tutor.objects.create(
                user=user,
                expertise=self.cleaned_data["expertise"],
                bio=self.cleaned_data.get("bio", "")
            )
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'level', 'is_free']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }