from django.db import models
# Create your models here.

difficulty_choices = (('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced'))

class Course(models.Model):
    title = models.CharField(max_length=100,blank=False,null=False)
    description = models.TextField(max_length=35,blank=False,null=False)
    difficulty = models.CharField(max_length=20, choices=difficulty_choices)
    learners = models.IntegerField(default=0)

class Module(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    description = models.TextField()
    course = models.ForeignKey(Course,related_name="courses",on_delete=models.CASCADE)

class Lesson(models.Model):
    module = models.ForeignKey(Module,related_name="lessons",on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=False,blank=False)
    content = models.TextField(blank=False,null=False)
    media = models.FileField(upload_to="lessonmedia")
    completed = models.BooleanField(default=False)

class Quiz(models.Model):
    module = models.OneToOneField(Module,related_name="quiz",on_delete=models.CASCADE)

class Questions(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, related_name="questions",on_delete=models.CASCADE)

class Options(models.Model):
    question = models.ForeignKey(Questions,related_name="options",on_delete=models.CASCADE)
    text = models.TextField()
    correct= models.BooleanField(null = False, blank= False)
    
class Exam(models.Model):
    course = models.OneToOneField(Course, related_name="exam", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Final Exam")
    pass_mark = models.IntegerField(default=80)  # percentage

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class ExamChoice(models.Model):
    question = models.ForeignKey(ExamQuestion, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)




