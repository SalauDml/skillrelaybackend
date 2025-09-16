# courses/seed_data.py

from accounts.models import AppUser
from courses.models import (
    Course, Module, Lesson, Quiz, Questions, Options,
    Exam, ExamQuestion, ExamChoice, UserCourseProgress
)


def run():


    # -------------------------
    # Course 1: Python for Beginners
    # -------------------------
    course1 = Course.objects.create(
        title="Python for Beginners",
        description="Learn Python step by step.",
        difficulty="beginner",
        learners=5,
    )

    # Modules
    module1_1 = Module.objects.create(
        title="Introduction to Python",
        description="Covers basics like variables and data types.",
        course=course1,
    )
    module1_2 = Module.objects.create(
        title="Control Flow",
        description="Learn about if statements, loops, and logic.",
        course=course1,
    )

    # Lessons for module1_1
    Lesson.objects.create(
        module=module1_1,
        title="Hello World",
        content="Your first Python program!",
        media="lessonmedia/hello.mp4",
    )
    Lesson.objects.create(
        module=module1_1,
        title="Variables",
        content="How to store data in Python variables.",
        media="lessonmedia/variables.mp4",
    )

    # Lesson for module1_2
    Lesson.objects.create(
        module=module1_2,
        title="If Statements",
        content="Making decisions in code with if statements.",
        media="lessonmedia/ifstatements.mp4",
    )

    # Quiz for module1_1
    quiz1 = Quiz.objects.create(module=module1_1)
    q1 = Questions.objects.create(quiz=quiz1, text="What function prints text in Python?")
    Options.objects.create(question=q1, text="print()", correct=True)
    Options.objects.create(question=q1, text="echo()", correct=False)

    # Exam for course1
    exam1 = Exam.objects.create(course=course1, title="Python Final Exam", pass_mark=70)
    eq1 = ExamQuestion.objects.create(exam=exam1, text="What symbol is used for comments in Python?")
    ExamChoice.objects.create(question=eq1, text="#", is_correct=True)
    ExamChoice.objects.create(question=eq1, text="//", is_correct=False)

    # -------------------------
    # Course 2: Django Basics
    # -------------------------
    course2 = Course.objects.create(
        title="Django Basics",
        description="Learn how to build web apps with Django.",
        difficulty="intermediate",
        learners=10,
    )

    module2_1 = Module.objects.create(
        title="Getting Started with Django",
        description="Setup and first app.",
        course=course2,
    )
    module2_2 = Module.objects.create(
        title="Django Models",
        description="Learn how to create and use models.",
        course=course2,
    )

    Lesson.objects.create(
        module=module2_1,
        title="Install Django",
        content="How to install Django and start a project.",
        media="lessonmedia/install.mp4",
    )
    Lesson.objects.create(
        module=module2_1,
        title="Your First App",
        content="How to create your first Django app.",
        media="lessonmedia/firstapp.mp4",
    )
    Lesson.objects.create(
        module=module2_2,
        title="Creating Models",
        content="How to define and use models in Django.",
        media="lessonmedia/models.mp4",
    )

    quiz2 = Quiz.objects.create(module=module2_2)
    q2 = Questions.objects.create(quiz=quiz2, text="Which file do you define Django models in?")
    Options.objects.create(question=q2, text="models.py", correct=True)
    Options.objects.create(question=q2, text="views.py", correct=False)

    exam2 = Exam.objects.create(course=course2, title="Django Final Exam", pass_mark=75)
    eq2 = ExamQuestion.objects.create(exam=exam2, text="Which command creates migrations?")
    ExamChoice.objects.create(question=eq2, text="python manage.py makemigrations", is_correct=True)
    ExamChoice.objects.create(question=eq2, text="python manage.py migrate", is_correct=False)

    # -------------------------
    # Course 3: Data Science 101
    # -------------------------
    course3 = Course.objects.create(
        title="Data Science 101",
        description="Introduction to Data Science concepts.",
        difficulty="advanced",
        learners=20,
    )

    module3_1 = Module.objects.create(
        title="Data Analysis Basics",
        description="Covers NumPy and Pandas.",
        course=course3,
    )

    Lesson.objects.create(
        module=module3_1,
        title="Introduction to Pandas",
        content="Learn about Pandas for data analysis.",
        media="lessonmedia/pandas.mp4",
    )

    quiz3 = Quiz.objects.create(module=module3_1)
    q3 = Questions.objects.create(quiz=quiz3, text="Which Python library is best for tabular data?")
    Options.objects.create(question=q3, text="Pandas", correct=True)
    Options.objects.create(question=q3, text="Matplotlib", correct=False)

    exam3 = Exam.objects.create(course=course3, title="Data Science Final Exam", pass_mark=80)
    eq3 = ExamQuestion.objects.create(exam=exam3, text="Which library is used for numerical arrays?")
    ExamChoice.objects.create(question=eq3, text="NumPy", is_correct=True)
    ExamChoice.objects.create(question=eq3, text="Requests", is_correct=False)



    print("✅ Full dummy data created: 3 courses, modules, lessons, quizzes, exams, and progress.")
