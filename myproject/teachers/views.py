from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from courses.models import Course
from .models import Teacher
from .forms import TeacherForm

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
    courses = Course.objects.filter(
        status="active")
    form = TeacherForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        teacher = form.save()
        Course.objects.filter(id__in=request.POST.getlist("courses")).update(instructor=teacher)
        messages.success(request, f"{teacher.full_name} has been added successfully.")
        return redirect("teachers:teacher_lists")
    context = {
        "courses": courses,
        "form": form,
    }
    return render(request, 'teachers/add_teachers.html', context)


@login_required
# (login_url='accounts:login')
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

@login_required
def teacher_edit(request, teacher_id):
    courses = Course.objects.filter(
            status="active")
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    form = TeacherForm(request.POST or None, instance=teacher)
    if request.method == "POST" and form.is_valid():
        teacher = form.save()
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
        "courses": courses,
        "form": form,
    }
    return render(request, 'teachers/edit_teachers.html', context)

@login_required
@require_POST
@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.delete()
    return redirect("teachers:teacher_lists")



