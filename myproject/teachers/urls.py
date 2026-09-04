from django.urls import path
from . import views

app_name = "teachers"
urlpatterns = [      
            # started rendering teachers page
            
            path('index/', views.index, name='index'),  
            path('add-teachers/', views.add_teachers, name='add_teachers'),
            path('teacher-lists/', views.teacher_lists, name='teacher_lists'),
            path('teacher-details/<int:pk>', views.teacher_details, name='teacher_details'),
            path('teacher-edit/<int:teacher_id>/', views.teacher_edit, name='teacher_edit'),
            path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
]