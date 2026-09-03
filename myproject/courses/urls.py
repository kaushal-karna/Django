from django.urls import path
from . import views

app_name='courses'

urlpatterns = [
    # HttpResponse to show url is working fine. shows 'This is the course display page'.
    path('', views.course_display, name='course_display'),
    
    # From here courses url starts
    
    path('index/', views.index, name='index'),
    path('add-courses/', views.add_courses, name='add_courses'),
    path('course-lists/', views.course_lists, name='course_lists'),
    path('course-details/<int:pk>/', views.course_details, name='course_details'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
]
