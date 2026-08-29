from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def teachers_list(request):
    return HttpResponse("List of teachers will be displayed here.")

def teachers_about(request):
    return render(request, 'teachers/about.html')

def teachers_home(request):
    return render(request, 'teachers/home.html')