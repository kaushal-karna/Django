from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Student
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
    student = Student.objects.all()
    if request.method == "POST":
        student = Student.objects.create(
           student_id=request.POST.get("student_id"), 
           first_name=request.POST.get("first_name"), 
           last_name=request.POST.get("last_name"),
           email=request.POST.get("email"), 
           phone=request.POST.get("phone"), 
           date_of_birth=request.POST.get("date_of_birth"), 
           department=request.POST.get("department"), 
           program=request.POST.get("program"), 
           semester=request.POST.get("semester"), 
           status=request.POST.get("status"),
        )
        messages.success( request, f"{student.first_name} {student.last_name} has been added successfully." )
    return render(request, 'students/add_students.html')


@login_required
def student_lists(request):
    students = Student.objects.all().order_by("student_id")

    context={
        "students": students
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
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.student_id = request.POST.get("student_id")
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.date_of_birth = request.POST.get("date_of_birth")
        student.department = request.POST.get("department")
        student.program = request.POST.get("program")
        student.semester = request.POST.get("semester")
        student.status = request.POST.get("status")
        student.address = request.POST.get("address")
        student.personal_info = request.POST.get("personal_info")
        student.enrollment_year = request.POST.get("enrollment_year")

        student.save()

        messages.success(
            request,
            "Student details updated successfully."
        )

        return redirect("students:student_lists")

    context = {
        "student": student,
    }

    return render(request, "students/edit_students.html", context)


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(
        request,
        "Student deleted successfully."
    )
    return redirect("students:student_lists")

