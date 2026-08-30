from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def homepage(request):
    # return HttpResponse("Welcome to the homepage!")
    content = {
        'title': 'My Website - Kaushal Karn',
        'message': 'Welcome to the Landing Page!',
    }
    return render(request, 'home/home.html', content)

