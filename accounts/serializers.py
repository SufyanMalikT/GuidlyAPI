from rest_framework import serializers
from .models import CustomUser
from api.models import Student, Consultant

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password']

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Create user
        user = CustomUser(**validated_data, role=role)
        user.set_password(password)
        user.save()

        # Create linked profile
        if role == 'student':
            Student.objects.create(user=user, full_name=user.username, email=user.email)
            print("hello, world!")
        elif role == 'consultant':
            Consultant.objects.create(user=user, full_name=user.username,email=user.email)

        return user
