from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObatinPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api.permissions import IsAdmin,IsConsultant,IsStudent
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import CustomUserSerializer
from api.permissions import IsAdmin, IsStudent


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return CustomUser.objects.all()

        # students can only see themselves
        return CustomUser.objects.filter(id=user.id)

    def get_object(self):
        obj = super().get_object()

        # Admin can access anyone
        if self.request.user.role == 'admin':
            return obj

        # Non-admins can only access themselves
        if obj.id != self.request.user.id:
            self.permission_denied(
                self.request, message="You do not have permission to access this user."
            )

        return obj

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            permission_classes = [IsAdmin]

        elif self.action == 'create':
            permission_classes = [AllowAny]

        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObatinPairSerializer