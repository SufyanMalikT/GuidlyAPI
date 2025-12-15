from django.db import models
from django.conf import settings
# Create your models here.

from django.db import models

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    full_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_country = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name

class Consultant(models.Model):
    full_name = models.CharField(max_length=60)
    phone = models.BigIntegerField(unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(auto_now_add=True)

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='consultant_profile',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name
    
class Program(models.Model):
    name = models.CharField(max_length=60)
    program_type = models.CharField(max_length=60)
    duration_months = models.IntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student,related_name='applications', on_delete=models.CASCADE)
    program = models.ForeignKey(Program,related_name='applications', on_delete=models.CASCADE)
    consultant = models.ForeignKey(Consultant,related_name='applications', on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'program')

    def __str__(self):
        return f"{self.student.full_name} - {self.program.name}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student.full_name} - {self.amount}"
