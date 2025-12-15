from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
router = routers.SimpleRouter()
router.register(r'users',CustomUserViewSet,basename='users')
urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='obtain-token'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('',include(router.urls))
]