from django.urls import path
from . import views

app_name = "teachers"
urlpatterns = [      
            path('', views.teachers_list, name='teachers_list'),  
            path('home/', views.teachers_home, name='teachers_home'),
            path('about/', views.teachers_about, name='teachers_about'),       
            # started rendering teachers page
            
            path('teachers/', views.teachers, name='teachers'),
            path('teacher-details/', views.teacher_details, name='teachers_details'),
            path('index/', views.teachers_index, name='index'),  
            path('add-teachers/', views.add_teachers, name='add_teachers'),
]