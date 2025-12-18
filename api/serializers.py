# api/serializers.py
from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultant
        fields = '__all__'
        read_only_fields = ['user', 'joined_date']


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.PrimaryKeyRelatedField(
        queryset=University.objects.all(),
        source='university',
        write_only=True
    )

    class Meta:
        model = Program
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['student', 'consultant', 'status', 'application_date']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        if not hasattr(user, 'student_profile'):
            raise serializers.ValidationError("Only students can apply.")

        # consultant auto-assignment (simple round-robin)
        consultant = Consultant.objects.filter(is_active=True).order_by('?').first()
        if not consultant:
            raise serializers.ValidationError("No consultant available.")

        return Application.objects.create(
            student=user.student_profile,
            consultant=consultant,
            **validated_data
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
