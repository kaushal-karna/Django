from django.db import models

class Teacher(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("on_leave", "On Leave"),
    ]
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)

    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)

    experience = models.PositiveIntegerField(default=0)
    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    bio = models.TextField(blank=True)
    
    subject = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name = "teachers"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
