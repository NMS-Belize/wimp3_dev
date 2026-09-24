from functools import wraps
from django.core.exceptions import PermissionDenied

def company_app_required(app_label, permission=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                raise PermissionDenied

            company = getattr(request.user, "company", None)

            if not company:
                raise PermissionDenied

            if not company.apps.filter(
                app_label=app_label,
                is_active=True
            ).exists():
                raise PermissionDenied

            if permission and not request.user.has_perm(permission):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator