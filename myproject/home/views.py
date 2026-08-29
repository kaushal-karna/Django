from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def home(request):
    # return render(request, 'home.html')
    return HttpResponse("Hello, World!")

def homepage(request):
    # return HttpResponse("Welcome to the homepage!")
    content = {
        'title': 'My Website - Kaushal Karn',
        'message': 'Welcome to the Landing Page!',
    }
    return render(request, 'home/landing_page.html', content)

def about(request):
    return render(request, 'home/about_page.html')

def contact(request):
    return render(request, 'home/contact_page.html')

def blog(request):
    return render(request, 'home/blog_page.html')

def experience(request):
    return render(request, 'home/experience.html')

def certification(request):
    return render(request, 'home/certification.html')


