from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        
        # Allow login page itself
        login_path = settings.LOGIN_URL.lstrip('/')
        path = request.path_info.lstrip('/')

        if path.startswith(login_path):
            return None

        # Allow staff/admin/static/media if needed
        if path.startswith('api/'):
            return None
        
        # Allow staff/admin/static/media if needed
        if path.startswith('admin/'):
            return None

        if request.user.is_authenticated:
            return None

        return redirect(settings.LOGIN_URL)