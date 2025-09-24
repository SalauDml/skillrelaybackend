from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import AppUser
from courses.models import (
    Course, Module, Lesson,
    Quiz, Questions, Options,
    Exam, ExamQuestion, ExamChoice
)
from tutors.models import CoursesHosted

@receiver(post_save, sender=AppUser)
def give_tutor_permissions(sender, instance, created, **kwargs):
    """
    Automatically give tutors all permissions related to course content.
    """
    if instance.is_tutor:
        models_to_manage = [
            Course, Module, Lesson,
            Quiz, Questions, Options,
            Exam, ExamQuestion, ExamChoice
        ]

        for model in models_to_manage:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            instance.user_permissions.add(*perms)
