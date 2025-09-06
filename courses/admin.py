from django.contrib import admin
from .models import Course,Module,Lesson,Questions,Quiz,Options,Exam,ExamChoice,ExamQuestion
# Register your models here.
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Questions)
admin.site.register(Quiz)
admin.site.register(Options)
admin.site.register(Exam)
admin.site.register(ExamChoice)
admin.site.register(ExamQuestion)

