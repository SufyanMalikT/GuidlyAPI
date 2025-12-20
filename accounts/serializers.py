from rest_framework import serializers
from .models import CustomUser
from api.models import Student, Consultant
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObatinPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'first_name':self.user.first_name,
            'last_name':self.user.last_name,
            'role': self.user.role,
        }
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(required=False, allow_null=True)
    preferred_country = serializers.CharField(required=False, allow_null=True)
    date_of_birth = serializers.DateTimeField(required=False,allow_null=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password',
            'phone',
            'preferred_country',
            'date_of_birth'
        ]

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
        preferred_country = validated_data.pop('preferred_country', None)
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Create user
        user = CustomUser(**validated_data, role=role)
        user.set_password(password)
        user.save()

        # Create profile based on role
        if role == 'student':
            Student.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                phone=phone,
                preferred_country=preferred_country,
            )

        elif role == 'consultant':
            Consultant.objects.create(
                user=user,
                full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
                phone=phone,
            )

        return user

    def update(self, instance, validated_data):
        phone = validated_data.pop('phone', None)
        preferred_country = validated_data.pop('preferred_country', None)
        date_of_birth = validated_data.pop('date_of_birth',None)
        # Update CustomUser fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related profile
        if instance.role == 'student' and hasattr(instance, 'student_profile'):
            student = instance.student_profile
            if phone is not None:
                student.phone = phone
            if preferred_country is not None:
                student.preferred_country = preferred_country
            if date_of_birth is not None:
                student.date_of_birth = date_of_birth
            student.save()

        elif instance.role == 'consultant' and hasattr(instance, 'consultant_profile'):
            consultant = instance.consultant_profile
            if phone is not None:
                consultant.phone = phone
            consultant.save()

        return instance

