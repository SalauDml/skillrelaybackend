from django.db import models
from accounts.models import AppUser
from courses.models import Course
# Create your models here.
class Tutor (models.Model):
    user = models.OneToOneField(AppUser,on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.full_name

class CoursesHosted(models.Model):
    tutor = models.ForeignKey(Tutor,related_name="hosted_courses",on_delete=models.CASCADE)
    course = models.OneToOneField(Course,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.course.title 