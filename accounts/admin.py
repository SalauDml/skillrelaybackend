from django.contrib import admin
from .models import CertificationList,AppUser
# Register your models here.
admin.site.register(AppUser)
admin.site.register(CertificationList)