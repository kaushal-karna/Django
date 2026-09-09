# tasks/serializers.py
from rest_framework import serializers
from .models import Task, Project

class ProjectSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'task_count']
        read_only_fields = ['created_at']

    def get_task_count(self, obj):
        return obj.tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'priority', 'project', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)


from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs['email'].strip().lower()
        password = attrs['password']

        # Find user using email
        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Incorrect email or password."
            )

        # Authenticate using Django's username
        user = authenticate(
            request=self.context.get('request'),
            username=user_obj.get_username(),
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Incorrect email or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "User account is disabled."
            )

        attrs['user'] = user
        return attrs