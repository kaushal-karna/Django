from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'code', 'name', 'department', 'instructor', 'credits', 'duration',
            'semester', 'capacity', 'status', 'description',
        ]
