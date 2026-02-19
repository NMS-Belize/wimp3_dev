from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

class ReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.method in SAFE_METHODS
        )