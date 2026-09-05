from django.urls import path
from . import views

from .views import StudentListView

app_name='students'

urlpatterns = [

    path('index/', views.index, name='index'),
    path('add-students/', views.add_students, name='add_students'),
    path('student-lists/', views.student_lists, name='student_lists'),
    path('student-details/<int:pk>/', views.student_details, name='student_details'),
    path('student-edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    
    # Class Based Views
    path('students-lists-views/', StudentListView.as_view(), name='student_view'),


]