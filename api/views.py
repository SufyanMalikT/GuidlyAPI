# api/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from .permissions import *


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(user=user)
        if user.role == 'admin':
            return Student.objects.all()
        return Student.objects.none()


class ConsultantViewSet(ModelViewSet):
    serializer_class = ConsultantSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Consultant.objects.all()


class UniversityViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [IsAdmin]


class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Application.objects.filter(student=user.student_profile)
        if user.role == 'consultant':
            return Application.objects.filter(consultant=user.consultant_profile)
        return Application.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsStudent()]
        if self.action in ['update', 'partial_update']:
            return [IsConsultant()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Payment.objects.all()
