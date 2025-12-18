# api/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    full_name = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_country = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Consultant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='consultant_profile'
    )
    full_name = models.CharField(max_length=60)
    phone = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name


class Program(models.Model):
    DEGREE_CHOICES = (
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
    )

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='programs'
    )
    name = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    duration_years = models.DecimalField(max_digits=3, decimal_places=1)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    consultant = models.ForeignKey(
        Consultant,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    notes = models.CharField(max_length=255, blank=True, null=True)
    application_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'program')
        indexes = [
            models.Index(fields=['consultant', 'status']),
            models.Index(fields=['student']),
        ]

    def __str__(self):
        return f"{self.student.full_name} - {self.program.name}"


class Payment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.student.full_name} - {self.amount}"
