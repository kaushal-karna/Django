from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
from courses.models import Course 
from django.views.generic import ListView, CreateView
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StudentForm

# Create your views here.

@login_required
def index(request):
    students = Student.objects.all()
    student_id = students.values("student_id")
    total = students.count()
    active = students.filter(status='active').count()
    inactive = students.filter(status='inactive').count()
    departments = students.values("department").distinct().count()
        
    context = {
            "students": students,
            "student_id": student_id,
            "total": total,
            "active": active,
            "inactive": inactive,
            "departments": departments,  
                
            }
    return render(request, 'students/index.html', context)


@login_required
def add_students(request):
    courses = Course.objects.filter(status="active")
    form = StudentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            student = form.save()
            student.enrolled_courses.set(request.POST.getlist("courses"))
            messages.success(request, f"{student.full_name} has been added successfully.")
            return redirect("students:student_lists")
    
    context = {
        "courses": courses,
        "form": form,
    }
    return render(request, 'students/add_students.html', context)


@login_required
def student_lists(request):
    students = Student.objects.all().order_by("student_id")
    departments = (
        Student.objects
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    context = {
        "students": students,
        "departments": departments,
        "status_choices": Student.STATUS_CHOICES,
    }
    return render(request, 'students/student_lists.html', context)


@login_required
def student_details(request, pk):
    
    student = get_object_or_404(Student, pk=pk)
    students = Student.objects.all()
    context = {
        "student": student,
        "students": students
    }
    
    return render(request, 'students/student_details.html', context)



@login_required
def student_edit(request, student_id):
    
    student = get_object_or_404(
        Student, 
        pk=student_id
        )
    courses = Course.objects.filter(status="active")
    
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        student = form.save()
        student.enrolled_courses.set(request.POST.getlist("courses"))
        messages.success(
            request,
            f"{student.full_name} has been updated successfully."
        )

        return redirect("students:student_lists")

    context = {
        "student": student,
        "courses":courses,
        "form": form,
    }

    return render(request, "students/edit_students.html", context)


@require_POST
@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(
        request,
        f"{student.full_name} has been deleted successfully."
    )
    return redirect("students:student_lists")




class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/students_lists_cbv.html"
    context_object_name = 'students'
    ordering = ['first_name']
    paginate_by = 10
    
    
class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'department', 'program', 'semester', 'status', 'address', 'personal_info']