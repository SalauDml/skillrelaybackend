from django.core.management.base import BaseCommand
from accounts.models import AppUser
from courses.models import (
    Course, Module, Lesson, Quiz, Questions, Options,
    Exam, ExamQuestion, ExamChoice, UserCourseProgress
)

class Command(BaseCommand):
    help = "Seed the database with dummy courses, modules, lessons, quizzes, and exams"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Clear old data
        UserCourseProgress.objects.all().delete()
        ExamChoice.objects.all().delete()
        ExamQuestion.objects.all().delete()
        Exam.objects.all().delete()
        Options.objects.all().delete()
        Questions.objects.all().delete()
        Quiz.objects.all().delete()
        Lesson.objects.all().delete()
        Module.objects.all().delete()
        Course.objects.all().delete()


        # === COURSES ===
        django_course = Course.objects.create(
            title="Django Basics",
            description="Learn the fundamentals of Django web development.",
            difficulty="beginner",
            learners=120
        )
        next_course = Course.objects.create(
            title="Frontend with Next.js",
            description="Get started with modern frontend development using Next.js.",
            difficulty="intermediate",
            learners=80
        )
        ai_course = Course.objects.create(
            title="Intro to AI",
            description="Understand basic AI concepts and machine learning.",
            difficulty="advanced",
            learners=60
        )

        # === MODULES & LESSONS (Django course) ===
        mod1 = Module.objects.create(course=django_course, title="Introduction", description="Getting started with Django")
        mod2 = Module.objects.create(course=django_course, title="Models", description="Learn about Django models")

        Lesson.objects.create(module=mod1, title="What is Django?", content="Django is a Python web framework.", media="lessonmedia/django1.mp4")
        Lesson.objects.create(module=mod1, title="Project Setup", content="Setting up a Django project.", media="lessonmedia/django2.mp4")

        Lesson.objects.create(module=mod2, title="Defining Models", content="Creating Django models.", media="lessonmedia/django3.mp4")
        Lesson.objects.create(module=mod2, title="Migrations", content="Running migrations in Django.", media="lessonmedia/django4.mp4")

        # === QUIZ for Module 2 (Django Models) ===
        quiz = Quiz.objects.create(module=mod2)
        q1 = Questions.objects.create(quiz=quiz, text="What command creates migrations?")
        Options.objects.create(question=q1, text="python manage.py makemigrations", correct=True)
        Options.objects.create(question=q1, text="python manage.py runserver", correct=False)

        q2 = Questions.objects.create(quiz=quiz, text="Which field creates an auto ID?")
        Options.objects.create(question=q2, text="AutoField", correct=True)
        Options.objects.create(question=q2, text="CharField", correct=False)

        # === EXAM for Django course ===
        exam = Exam.objects.create(course=django_course, title="Final Exam", pass_mark=70)
        eq1 = ExamQuestion.objects.create(exam=exam, text="Django follows which pattern?")
        ExamChoice.objects.create(question=eq1, text="MVC", is_correct=False)
        ExamChoice.objects.create(question=eq1, text="MTV", is_correct=True)

        eq2 = ExamQuestion.objects.create(exam=exam, text="Which file stores installed apps?")
        ExamChoice.objects.create(question=eq2, text="settings.py", is_correct=True)
        ExamChoice.objects.create(question=eq2, text="urls.py", is_correct=False)

        # === MODULES & LESSONS (Next.js course) ===
        mod3 = Module.objects.create(course=next_course, title="Setup", description="Getting started with Next.js")
        Lesson.objects.create(module=mod3, title="Installing Next.js", content="Using npx create-next-app.", media="lessonmedia/next1.mp4")
        Lesson.objects.create(module=mod3, title="Pages in Next.js", content="Understanding the pages router.", media="lessonmedia/next2.mp4")

        # === MODULES & LESSONS (AI course) ===
        mod4 = Module.objects.create(course=ai_course, title="AI Basics", description="Introduction to Artificial Intelligence")
        Lesson.objects.create(module=mod4, title="What is AI?", content="AI is intelligence demonstrated by machines.", media="lessonmedia/ai1.mp4")
        Lesson.objects.create(module=mod4, title="Machine Learning", content="Intro to supervised and unsupervised learning.", media="lessonmedia/ai2.mp4")

        # === USER PROGRESS ===

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete with courses, lessons, quizzes, exams, and user progress!"))
