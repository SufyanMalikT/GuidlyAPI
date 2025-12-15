from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated and request.user.is_student)
        return request.user.is_authenticated and request.user.is_student
    

class IsConsultant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_consultant
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
    