from django.contrib import admin
from .models import Tutor, CoursesHosted


class TutorRestrictedAdminMixin:
    """
    Restricts tutors in the admin to only see themselves
    and their hosted courses.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusers see all
        if request.user.is_superuser:
            return qs

        # Tutor users only see their own data
        if hasattr(request.user, "tutor"):
            # If managing Tutor model → return only themselves
            if self.model is Tutor:
                return qs.filter(user=request.user)

            # If managing CoursesHosted → return only their hosted courses
            if self.model is CoursesHosted:
                return qs.filter(tutor=request.user.tutor)

        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and hasattr(request.user, "tutor"):
            if isinstance(obj, Tutor):
                return obj.user == request.user
            if isinstance(obj, CoursesHosted):
                return obj.tutor == request.user.tutor
        return False

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


@admin.register(Tutor)
class TutorAdmin(TutorRestrictedAdminMixin, admin.ModelAdmin):
    list_display = ("user", "bio")


@admin.register(CoursesHosted)
class CoursesHostedAdmin(TutorRestrictedAdminMixin, admin.ModelAdmin):
    list_display = ("course", "tutor")
