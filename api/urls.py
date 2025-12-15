from django.urls import path, include
from .views import StudentViewSet,ConsultantViewSet, ProgramViewSet, ApplicationViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'applications',ApplicationViewSet,basename='application')
router.register(r'students',StudentViewSet,basename='students')
router.register(r'consultants',ConsultantViewSet,basename='consultants')
router.register(r'programs',ProgramViewSet,basename='programs')
urlpatterns = [
    path("api/",include(router.urls))
]