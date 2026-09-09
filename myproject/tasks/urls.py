# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectViewSet, DashboardView, CompletedTaskListView, LoginView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    # ViewSet URLs (Auto-generated)
    path('', include(router.urls)),
    
    # APIView URL (Manual)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Generic View URL (Manual)
    path('tasks/completed/', CompletedTaskListView.as_view(), name='completed-tasks'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
]