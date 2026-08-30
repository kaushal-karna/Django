from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def teachers_list(request):
    return HttpResponse("List of teachers will be displayed here.")

def teachers_about(request):
    return render(request, 'teachers/about.html')

def teachers_home(request):
    return render(request, 'teachers/home.html')

def teachers_index(request):
    return render(request, 'teachers/index.html',
    #             {
    #     "dashboard_type": "teachers"
    # }
    )

def add_teachers(request):
    return render(request, 'teachers/add-teachers.html')

def teachers(request):
    return render(request, 'teachers/teachers.html')

def teacher_details(request):
    return render(request, 'teachers/teacher-details.html')
