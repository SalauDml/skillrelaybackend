from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import os
from dotenv import load_dotenv
from cloudinary.models import CloudinaryField


class UserManager(BaseUserManager):
    def create_user(self,email, password,first_name,last_name,phone,**kwargs):
        if not email:
            raise ValueError("The email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email,phone= phone, first_name = first_name, last_name = last_name,**kwargs)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email,first_name,last_name,phone, password, **extra_fields)



class AppUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, null= False,blank=False)
    last_name = models.CharField(max_length=150, null=False,blank=False)
    middle_name = models.CharField(max_length=150, null=True, blank= True)
    email= models.EmailField(unique=True)
    phone = PhoneNumberField(blank= True, null= True)
    location = models.CharField(max_length=100,blank=False)
    profile_picture = CloudinaryField(blank = True, null = True, type="upload", resource_type = "image")
    is_tutor = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name','first_name','phone']
    
    objects = UserManager()

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.email} - {status}"

class CertificationList(models.Model):
    user = models.ForeignKey(AppUser,related_name='files',on_delete=models.CASCADE)
    file = models.FileField(upload_to='certificationfiles/')

    def __str__(self):
        return self.file.name
    
