from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.template import context
from django.contrib import messages
from courses.models import Course
from .models import Teacher

# Create your views here.
@login_required
def index(request): 
    teachers = Teacher.objects.all()
    total = teachers.count()
    active = teachers.filter(status='active').count()
    inactive = teachers.filter(status='inactive').count()
    departments = teachers.values("department").distinct().count()
            
    context = {
                "teachers": teachers,
                "total": total,
                "active": active,
                "inactive": inactive,
                "departments": departments,  
                    
                }
    return render(request, 'teachers/index.html', context)


@login_required
def add_teachers(request):
    if request.method == "POST":
        courses = Course.objects.filter(
        status="active")
        print("========== POST DATA ==========")

        for key, value in request.POST.items():
            print(key, "=>", value)

        print("===============================")


        teacher = Teacher.objects.create(
            teacher_id=request.POST.get("teacher_id"),
            first_name=request.POST.get("first_name"), 
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"), 
            phone=request.POST.get("phone"), 
            joining_date=request.POST.get("joining_date"), 
            department=request.POST.get("department"), 
            position=request.POST.get("position"),
            qualification=request.POST.get("qualification"),
            experience=request.POST.get("experience"),
            status=request.POST.get("status"),
            bio=request.POST.get("bio"),         
        )
        
        course_ids = request.POST.getlist("courses")

        Course.objects.filter(
            id__in=course_ids
        ).update(
            instructor=teacher
        )
        messages.success(
            request,
            f"{teacher.full_name} has been added successfully.")
        return redirect("teachers:teacher_lists")  
    return render(request, 'teachers/add_teachers.html')


@login_required
def teacher_lists(request):
    teachers = Teacher.objects.all().order_by("teacher_id")
    
    context={
            "teachers": teachers
        }
    return render(request, 'teachers/teacher_lists.html', context)


@login_required
def teacher_details(request, pk):
    teachers = get_object_or_404(Teacher, pk=pk)
    teacher = Teacher.objects.all()
    context = {
        "teacher": teacher,
        "teachers": teachers,
        
    }   
    return render(request, 'teachers/teacher_details.html', context)


def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == "POST":
        teacher.teacher_id = request.POST.get("teacher_id")
        teacher.first_name = request.POST.get("first_name")
        teacher.last_name = request.POST.get("last_name")
        teacher.email = request.POST.get("email")
        teacher.phone = request.POST.get("phone")
        teacher.joining_date = request.POST.get("joining_date")
        teacher.department = request.POST.get("department")
        teacher.position = request.POST.get("position")
        teacher.qualification = request.POST.get("qualification")
        teacher.experience = request.POST.get("experience")
        teacher.status = request.POST.get("status")
        teacher.bio = request.POST.get("bio")
        
        teacher.save()
        course_ids = request.POST.getlist("courses")

        # Remove courses previously assigned to this teacher
        teacher.courses.update(
            instructor=None
        )

        # Assign selected courses to this teacher
        Course.objects.filter(
            id__in=course_ids
        ).update(
            instructor=teacher
        )
        
        messages.success(
            request,
            f"{ teacher.full_name } has been updated successfully"
        )
        return redirect('teachers:teacher_lists')
    
    context = {
        "teacher": teacher,
    }
    return render(request, 'teachers/edit_teachers.html', context)

def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect("teachers:teacher_lists")



