from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self,email, password,full_name, phone_number,**kwargs):
        if not email:
            raise ValueError("The email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email,phone_number= phone_number, full_name = full_name,**kwargs)
        user.set_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self, email, full_name, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password,full_name,phone_number, **extra_fields)



class AppUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, null= False,blank=False)
    last_name = models.CharField(max_length=150, null=False,blank=False)
    middle_name = models.CharField(max_length=150, null=True, blank= True)
    email= models.EmailField(unique=True)
    phone = PhoneNumberField(blank= True, null= True)
    location = models.CharField(max_length=100,blank=False)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=False)
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
        return super().__str__()
    
