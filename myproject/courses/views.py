from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def course_display(request):
    return HttpResponse("This is the course display page.")

def courses_home(request):
    return render(request, 'home.html')

def courses_about(request):
    return render(request, 'about.html')