from django.shortcuts import render
from django.http import HttpResponse


def course_display(request):
    return HttpResponse("This is the course display page.")

def courses(request):
    return render(request, 'courses/courses.html')

def course_details(request):
    return render(request, 'courses/course-details.html')

def index(request):
    return render(request, 'courses/index.html')

def add_course(request):
    return render(request, 'courses/add-course.html')