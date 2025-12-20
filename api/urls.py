from django.urls import path, include
from .views import (
    StudentViewSet,ConsultantViewSet, ProgramViewSet, 
    ApplicationViewSet, PaymentViewSet, UniversityViewSet)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'applications',ApplicationViewSet,basename='application')
router.register(r'students',StudentViewSet,basename='students')
router.register(r'consultants',ConsultantViewSet,basename='consultants')
router.register(r'programs',ProgramViewSet,basename='programs')
router.register(r'payments',PaymentViewSet, basename='payments')
router.register(r'universities',UniversityViewSet,basename='universities')
urlpatterns = [
    path("api/",include(router.urls))
]