from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student','Student'),
        ('consultant','Consultant'),
        ('admin','Admin')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    @property
    def is_student(self):
        return self.role == 'student'
    
    @property    
    def is_consultant(self):
        return self.role == 'consultant'
    
    @property    
    def is_admin(self):
        return self.role == 'admin'
