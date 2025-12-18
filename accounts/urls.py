from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView 
router = routers.SimpleRouter()
router.register(r'users',CustomUserViewSet,basename='users')
urlpatterns = [
    path('token/',CustomTokenObtainPairView.as_view(),name='obtain-token'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),
    path('',include(router.urls))
]