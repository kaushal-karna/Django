from rest_framework import serializers
from .models import Student
class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'department', 'program', 'semester', 'status', 'address', 'personal_info', 'created_at', 'updated_at']
        read_only_fields = ['student_id', 'created_at', 'updated_at', 'date_of_birth']
        
    # Custom validation
    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    