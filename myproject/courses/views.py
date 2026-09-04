from django.shortcuts import render, redirect, get_object_or_404    
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Course
from teachers.models import Teacher
from django.contrib import messages

# Showing text in httpresponse 

def course_display(request):
    total_course = Course.objects.count()
    return HttpResponse("This is the course display page.")

# from here course pages are made

@login_required
def index(request): 
    courses = Course.objects.all()
    total = courses.count()
    active = courses.filter(status='active').count()
    inactive = courses.filter(status='inactive').count()
    departments = courses.values("department").distinct().count()
    code = courses.values("code")
    print(f"Total Courses: {total}")
    
    context = {
        "courses": courses,
        "total": total,
        "active": active,
        "inactive": inactive,
        "departments": departments,  
        "code": code,             
        }
    return render(request, 'courses/index.html', context)

@login_required
def add_courses(request):
    teachers = Teacher.objects.filter(status="active")
    if request.method == "POST":
        courses = Course.objects.create(
            code=request.POST.get("code"),
            name=request.POST.get("name"),
            department=request.POST.get("department"),
            instructor_id=request.POST.get("instructor"),
            credits=request.POST.get("credits"),
            duration=request.POST.get("duration"),
            semester=request.POST.get("semester"),
            capacity=request.POST.get("capacity"),
            status=request.POST.get("status"),
            description=request.POST.get("description"),
        )
        
        messages.success(request,
            f"{ courses.code } { courses.name } has been added successfully."
        )
        return redirect('courses:course_lists')
    context = {
        "teachers": teachers
    }
      
    return render(request, 'courses/add_courses.html', context)

@login_required
def course_lists(request):
    courses = Course.objects.all()
    departments = (
        Course.objects
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    context = {
        "courses": courses,
        "departments": departments,
        "status_choices": Course.STATUS_CHOICES,
    }
    return render(request, 'courses/course_lists.html', context)


@login_required
def course_details(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {
        "course": course
        }
    return render(request, 'courses/course_details.html', context)





def edit_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    teachers = Teacher.objects.filter(
        status="active"
    )

    if request.method == "POST":

        course.code = request.POST.get("code")
        course.name = request.POST.get("name")
        course.department = request.POST.get("department")
        course.instructor_id = request.POST.get("instructor")
        course.credits = request.POST.get("credits")
        course.duration = request.POST.get("duration")
        course.semester = request.POST.get("semester")
        course.capacity = request.POST.get("capacity")
        course.status = request.POST.get("status")
        course.description = request.POST.get("description")

        course.save()
        
        messages.success(
                    request,
                    f"{course.code} has been updated successfully."
                )

        return redirect("courses:course_lists")

    context = {
        "course": course,
        "teachers": teachers,
    }

    return render(
        request,
        "courses/course_edit.html",
        context
    )


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(
        request,
        f"{course.code} {course.name} has been deleted successfully"
    )
    return redirect("courses:course_lists")




