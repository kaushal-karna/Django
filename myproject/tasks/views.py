from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task, Project
from .serializers import TaskSerializer, ProjectSerializer
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # SECURITY: Only return tasks belonging to the current user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Extra safety: Ensure owner is set during creation
        serializer.save(owner=self.request.user)


# --- METHOD 1: ModelViewSet (Standard CRUD) ---
class ProjectViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Projects.
    Automatically generates: list, create, retrieve, update, partial_update, destroy
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# --- METHOD 2: APIView (Custom Logic) ---
@extend_schema(description="Dashboard API")
class DashboardView(APIView):
    """
    Custom endpoint that aggregates data from multiple models.
    Use APIView when you need full control over the request/response cycle.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
       
        # Custom aggregation logic
        total_tasks = Task.objects.filter(owner=user).count()
        completed_tasks = Task.objects.filter(owner=user, is_completed=True).count()
        active_projects = Project.objects.filter(owner=user).count()
       
        data = {
            "user": user.username,
            "stats": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": f"{(completed_tasks/total_tasks*100) if total_tasks > 0 else 0:.1f}%",
                "active_projects": active_projects
            }
        }
        return Response(data)

# --- METHOD 3: Generic View (Specialized List) ---

class CompletedTaskListView(generics.ListAPIView):
    """
    Uses a Generic View for a specific filtered list.
    More concise than APIView for simple read-only operations.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user, is_completed=True)


# tasks/views.py
from drf_spectacular.utils import extend_schema

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "token_type": {"type": "string"},
                    "user_id": {"type": "integer"},
                    "email": {"type": "string"},
                },
            }
        },
    )

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Get existing token or create a new one
        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                'access_token': token.key,
                'token_type': 'Token',
                'user_id': user.id,
                'email': user.email,
            },
            status=status.HTTP_200_OK,
        )