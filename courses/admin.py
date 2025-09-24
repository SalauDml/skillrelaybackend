from django.contrib import admin
from .models import Course,Module,Lesson,Questions,Quiz,Options,Exam,ExamChoice,ExamQuestion,UserCourseProgress,CompletedCourse,CourseCategory
# Register your models here.
# admin.site.register(Course)
# admin.site.register(Module)
# admin.site.register(Lesson)
# admin.site.register(Questions)
# admin.site.register(Quiz)
# admin.site.register(Options)
# admin.site.register(Exam)
# admin.site.register(ExamChoice)
# admin.site.register(ExamQuestion)
# admin.site.register(UserCourseProgress)
# admin.site.register(CompletedCourse)
# admin.site.register(CourseCategory)
# All models from .models have been registered already.

# courses/admin.py
from django.contrib import admin
# from tutors.admin_mixins import TutorRestrictedMixin
from .models import Course, Module, Lesson, Quiz, Questions, Options, Exam, ExamQuestion, ExamChoice
from tutors.models import CoursesHosted

# courses/admin.py
from django.contrib import admin
from tutors.models import Tutor
from .models import (
    Course, Module, Lesson, Quiz, Questions, Options,
    Exam, ExamQuestion, ExamChoice
)

class TutorRestrictedMixin:
    """
    Restrict tutors to only see/edit objects they created (through their hosted courses).
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        # superusers see everything
        if user.is_superuser:
            return qs

        # tutors see only their own content
        if hasattr(user, "tutor"):
            filter_map = {
                "course": {"courseshosted__tutor__user": user},
                "module": {"course__courseshosted__tutor__user": user},
                "lesson": {"module__course__courseshosted__tutor__user": user},
                "quiz": {"module__course__courseshosted__tutor__user": user},
                "questions": {"quiz__module__course__courseshosted__tutor__user": user},
                "options": {"question__quiz__module__course__courseshosted__tutor__user": user},
                "exam": {"course__courseshosted__tutor__user": user},
                "examquestion": {"exam__course__courseshosted__tutor__user": user},
                "examchoice": {"question__exam__course__courseshosted__tutor__user": user},
            }

            model_name = self.model._meta.model_name
            if model_name in filter_map:
                return qs.filter(**filter_map[model_name])

        # non-tutors get nothing
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, "tutor") and obj is not None:
            # For Course model
            if self.model._meta.model_name == "course":
                try:
                    return hasattr(obj, "courseshosted") and obj.courseshosted.tutor.user == request.user
                except Exception:
                    return False
            # For related models, allow if the related course is hosted by this tutor
            # (You can expand this logic for other models as needed)
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, "tutor")


@admin.register(Course)
class CourseAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        # show only courses hosted by this tutor
        return qs.filter(courseshosted__tutor__user=user)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Ensure CoursesHosted is created for this course and tutor
        if hasattr(request.user, "tutor") and not request.user.is_superuser:
            from tutors.models import CoursesHosted
            CoursesHosted.objects.get_or_create(tutor=request.user.tutor, course=obj)


@admin.register(Module)
class ModuleAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(course__hosted_course__tutor__user=user)

    def assign_tutor(self, obj, user):
        # tutor already tied via course → no need to set
        pass

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lesson)
class LessonAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(module__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "module" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import Module
            kwargs["queryset"] = Module.objects.filter(course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Quiz)
class QuizAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(module__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "module" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import Module
            kwargs["queryset"] = Module.objects.filter(course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Questions)
class QuestionsAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(quiz__module__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "quiz" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import Quiz
            kwargs["queryset"] = Quiz.objects.filter(module__course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Options)
class OptionsAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(question__quiz__module__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import Questions
            kwargs["queryset"] = Questions.objects.filter(quiz__module__course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Exam)
class ExamAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExamQuestion)
class ExamQuestionAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(exam__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "exam" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import Exam
            kwargs["queryset"] = Exam.objects.filter(course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ExamChoice)
class ExamChoiceAdmin(TutorRestrictedMixin, admin.ModelAdmin):
    def filter_for_tutor(self, qs, user):
        return qs.filter(question__exam__course__hosted_course__tutor__user=user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question" and hasattr(request.user, "tutor") and not request.user.is_superuser:
            from .models import ExamQuestion
            kwargs["queryset"] = ExamQuestion.objects.filter(exam__course__courseshosted__tutor__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
