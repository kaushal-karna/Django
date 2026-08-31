from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from datetime import datetime


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.

def students_home(request):
    return render(request, 'home.html')

def students_about(request):
    return render(request, 'about.html')


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


def student_list(request):
    students = [
          {'name': 'Ram', 'age': 21, 'course': 'CSIT'},
          {'name': 'Sita', 'age': 22, 'course': 'BBA'},
          {'name': 'Hari', 'age': 20, 'course': 'BSc IT'},
      ]
     
    context = {
          'page_title': 'Student List',
          'students': students,
          'total_students': len(students),
          'current_date': datetime.now(),
          'user': request.user,
      }
     
    return render(request, 'students/student_list.html', context)


def index(request):
    return render(request, 'students/index.html')