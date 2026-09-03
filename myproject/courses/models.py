from django.db import models


# Create your models here.



class Course(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    SEMESTER_CHOICES = [
        ("Spring 2026", "Spring 2026"),
        ("Fall 2026", "Fall 2026"),
        ("Spring 2027", "Spring 2027"),
        ("Fall 2027", "Fall 2027"),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    instructor = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name= "courses"
    )
    credits = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)
    enrolled_students = models.ManyToManyField(
        "students.Student",
        blank=True,
        related_name="enrolled_courses"
    )
    semester = models.CharField(
        max_length=20,
        choices=SEMESTER_CHOICES
    )
    capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
    )
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"