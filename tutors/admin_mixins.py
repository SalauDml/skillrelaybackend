# tutors/admin_mixins.py
from django.core.exceptions import PermissionDenied

class TutorRestrictedMixin:
    """
    Restricts queryset and saves so tutors only see/edit their own courses
    and everything related to them.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_tutor:
            return self.filter_for_tutor(qs, request.user)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if request.user.is_tutor:
            self.assign_tutor(obj, request.user)
        super().save_model(request, obj, form, change)

    # ---- Helpers you override per model ----
    def filter_for_tutor(self, qs, user):
        """Return qs filtered to objects belonging to this tutor."""
        raise NotImplementedError

    def assign_tutor(self, obj, user):
        """Attach tutor to newly created objects when needed."""
        pass
