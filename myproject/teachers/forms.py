from django import forms

from .models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'teacher_id', 'first_name', 'last_name', 'email', 'phone',
            'department', 'position', 'qualification', 'experience',
            'joining_date', 'status', 'bio',
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }
