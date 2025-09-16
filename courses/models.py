from django.db import models
from accounts.models import AppUser
# Create your models here.

difficulty_choices = (('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced'))


class Course(models.Model):
    title = models.CharField(max_length=100,blank=False,null=False)
    description = models.TextField(max_length=35,blank=False,null=False)
    difficulty = models.CharField(max_length=20, choices=difficulty_choices)
    learners = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField()
    course = models.ForeignKey(Course,related_name="modules",on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module,related_name="lessons",on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False,blank=False)
    content = models.TextField(blank=False,null=False)
    media = models.FileField(upload_to="lessonmedia",null= True, blank= True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    module = models.OneToOneField(Module,related_name="quiz",on_delete=models.CASCADE)

    def __str__(self):
        return f"Quiz for {self.module.title}"

class Questions(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, related_name="questions",on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Options(models.Model):
    question = models.ForeignKey(Questions,related_name="options",on_delete=models.CASCADE)
    text = models.TextField()
    correct= models.BooleanField(null = False, blank= False)
    
    def __str__(self):
        return self.text

class Exam(models.Model):
    course = models.OneToOneField(Course, related_name="exam", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Final Exam")
    pass_mark = models.IntegerField(default=80)  # percentage

    def __str__(self):
        return self.title

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class ExamChoice(models.Model):
    question = models.ForeignKey(ExamQuestion, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserCourseProgress(models.Model):
    user = models.ForeignKey(AppUser,on_delete=models.CASCADE,related_name="course_progress")
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    current_module = models.ForeignKey(Module,on_delete=models.SET_NULL, null= True)
    current_lesson = models.ForeignKey(Lesson,on_delete=models.SET_NULL, null = True)

    def __str__(self):
        return f"{self.user.full_name} - {self.course.title}"





