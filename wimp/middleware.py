from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware to require login for all non-public pages,
    while bypassing API requests and static/admin resources.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before reaching the view
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info  # full path including leading slash

        # 1️⃣ Bypass all API requests (token/JWT/API key)
        if path.startswith('/api/'):
            return None  # DRF handles authentication

        # 2️⃣ Allow OPTIONS preflight requests anywhere
        if request.method == 'OPTIONS':
            return None

        # 3️⃣ Allow login page itself
        if path.startswith(settings.LOGIN_URL):
            return None

        # 4️⃣ Allow admin pages
        if path.startswith('/admin/'):
            return None

        # 5️⃣ Allow static and media files
        if path.startswith('/static/') or path.startswith('/media/'):
            return None

        # 6️⃣ Allow authenticated users for normal pages
        if request.user.is_authenticated:
            return None

        # 7️⃣ Everything else → redirect to login page
        return redirect(settings.LOGIN_URL)


'''from sys import path
from urllib import request
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        path = request.path_info
        
        # 1. Allow staff/admin/static/media if needed
        if path.startswith('api/'):
            return None
        
        # Allow OPTIONS requests to API (CORS preflight)
        if request.method == 'OPTIONS':
            return None
        
        # Allow DRF API views (Token / JWT / API key auth)
        #if issubclass(getattr(view_func, 'view_class', object), APIView):
        #    return None

        # 2. Allow login page
        login_path = settings.LOGIN_URL
        if path.startswith(login_path):
            return None

        # 3. Allow staff/admin/static/media if needed
        if path.startswith('admin/'):
            return None
        
        # 4. Allow static & media
        if path.startswith('static/') or path.startswith('media/'):
            return None

        # 5. Allow authenticated users
        if request.user.is_authenticated:
            return None

        # 6. Everything else → redirect to login
        return redirect(settings.LOGIN_URL)'''