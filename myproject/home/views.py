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

students = [{
        "student_id": 1,
        "name": "Kaushal Karn",
        "age": 20,
        "grade": "A",
        "course": "Computer Science"
    }, 
                {
        "student_id": 2,
        "name": "John Doe",
        "age": 22,
        "grade": "B",
        "course": "Mathematics"
    },
                {
        "student_id": 3,
        "name": "harry Potter",
        "age": 20,
        "grade": "A",
        "course": "Computer Science"
    }
        ,        {
        "student_id": 4,
        "name": "Jane Smith",
        "age": 19,
        "grade": "B",
        "course": "Physics"
    }
    ]

def student_display(request):
    # stu = dict(students)
    return JsonResponse(students, safe=False)

def student_detail(request, student_id): 
    for student in students:
        if student["student_id"] == student_id:
            return JsonResponse(student)
            
            # return HttpResponse(student)     
    return HttpResponse("Student not found.")
    