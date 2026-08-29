from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    # return render(request, 'home.html')
    return HttpResponse("Hello, World!")

def homepage(request):
    # return HttpResponse("Welcome to the homepage!")
    content = {
        'title': 'My Website -Kaushal Karn',
        'message': 'Welcome to the homepage! -Kaushal Karn',
    }
    return render(request, 'home/home.html', content)

def about(request):
    return render(request, 'home/about.html')

