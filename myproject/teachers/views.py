from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from django.template import context

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
    return render(request, 'teachers/add_teachers.html')


@login_required
def teacher_lists(request):
    teachers = Teacher.objects.all().order_by("first_name")
    
    context={
            "teachers": teachers
        }
    return render(request, 'teachers/teacher_lists.html', context)


@login_required
def teacher_details(request):
    return render(request, 'teachers/teacher_details.html')


def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    
    if request.method == "POST":
        teacher.code = request.POST.get("id")
        teacher.first_name = request.POST.get("first_name")
        teacher.last_name = request.POST.get("last_name")
        teacher.email = request.POST.get("email")
        teacher.phone = request.POST.get("phone")
        teacher.department = request.POST.get("department")
        teacher.position = request.POST.get("position")
        teacher.qualification = request.POST.get("qualification")
        teacher.experience = request.POST.get("experience")
        teacher.status = request.POST.get("status")
        teacher.bio = request.POST.get("bio")
        teacher.subject = get_object_or_404(Course, pk=request.POST.get('subject'))
        teacher.save()
        return redirect('teachers:teacher_lists')
    
    context = {
        "teacher": teacher
    }
    return render(request, 'teachers/edit_teachers.html', context)

def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect("teachers:teacher_lists")



