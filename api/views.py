from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Student, Consultant, Program, Application, Payment
from .serializers import (
    StudentSerializer, ConsultantSerializer,
    ProgramSerializer, ApplicationSerializer,
    PaymentSerializer
)
from .permissions import IsStudent, IsConsultant, IsAdmin


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_student', False) and hasattr(user, 'student_profile'):
            # Student sees only their own record
            return Student.objects.filter(pk=user.student_profile.pk)
        elif getattr(user, 'is_consultant', False):
            # Consultant sees all students assigned via applications
            return Student.objects.filter(application__consultant=user.consultant_profile).distinct()
        elif getattr(user, 'is_admin', False):
            return Student.objects.all()
        return Student.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]  # Only admin can modify student records
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ConsultantViewSet(ModelViewSet):
    queryset = Consultant.objects.all()
    serializer_class = ConsultantSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_consultant', False) and hasattr(user, 'consultant_profile'):
            # Consultant sees only their own profile
            return Consultant.objects.filter(pk=user.consultant_profile.pk)
        elif getattr(user, 'is_admin', False):
            return Consultant.objects.all()
        return Consultant.objects.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]  # Only admin can modify consultant records
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:  # list and retrieve
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_student', False) and hasattr(user, 'student_profile'):
            # Student sees only their own applications
            return Application.objects.filter(student=user.student_profile)
        elif getattr(user, 'is_consultant', False) and hasattr(user, 'consultant_profile'):
            # Consultant sees only applications assigned to them
            return Application.objects.filter(consultant=user.consultant_profile)
        elif getattr(user, 'is_admin', False):
            return Application.objects.all()
        return Application.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsStudent]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsConsultant]
        elif self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        if not getattr(user, 'is_student', False) or not hasattr(user, 'student_profile'):
            raise ValidationError("Only students can create applications.")
        serializer.save(student=user.student_profile)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_student', False) and hasattr(user, 'student_profile'):
            # Student sees only their own payments
            return Payment.objects.filter(student=user.student_profile)
        elif getattr(user, 'is_consultant', False) and hasattr(user, 'consultant_profile'):
            # Consultant sees payments related to applications assigned to them
            return Payment.objects.filter(application__consultant=user.consultant_profile)
        elif getattr(user, 'is_admin', False):
            return Payment.objects.all()
        return Payment.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]  # Only admins can modify payments
        else:
            permission_classes = [IsAuthenticated]  # list/retrieve for authenticated users
        return [permission() for permission in permission_classes]
