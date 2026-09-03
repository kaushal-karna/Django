from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime, date


class Student(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("graduated", "Graduated"),
        ("suspended", "Suspended"),
    ]

    SEMESTER_CHOICES = [
        ("Spring 2026", "Spring 2026"),
        ("Fall  2026", "Fall 2026"),
        ("Spring 2027", "Spring 2027"),
        ("Fall 2027", "Fall 2027"),
    ]

    student_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    students_enrolled = models.PositiveIntegerField(default=0, blank=True)
    date_of_birth = models.DateField()

    department = models.CharField(max_length=150)
    program = models.CharField(max_length=150)

    semester = models.CharField(
        max_length=20,
        choices=SEMESTER_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    address = models.TextField(blank=True)
    
    # Additional fields for student information
    personal_info = models.TextField(blank=True)
    CURRENT_YEAR = date.today().year
    YEAR_CHOICES = [(year, year) for year in range(2000, CURRENT_YEAR + 1)]
    
    enrollment_year = models.PositiveIntegerField(default=CURRENT_YEAR)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"