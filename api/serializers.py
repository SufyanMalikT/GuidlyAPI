from rest_framework import serializers
from .models import Student, Consultant, Program, Application, Payment
from accounts.serializers import CustomUserSerializer
class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['id']



class ConsultantSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Consultant
        fields = '__all__'
        read_only_fields = ['id']

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program 
        fields = '__all__'
        read_only_fields = ['id']

class ApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    consultant = ConsultantSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'student', 'consultant', 'program','status','notes','application_date']
        read_only_fields = ['id','student','application_date']

class PaymentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    consultant = ConsultantSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = ['id','application','student','amount','payment_method','status']