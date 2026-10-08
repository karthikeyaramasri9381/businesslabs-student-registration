import os
import uuid

from django.db import models


def aadhaar_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{extension}"
    return f"aadhaar/{filename}"


class Admin(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Student(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    qualification = models.CharField(max_length=100)
    interests = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    aadhaar = models.FileField(upload_to=aadhaar_upload_path)

    def __str__(self):
        return self.full_name