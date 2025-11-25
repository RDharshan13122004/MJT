from django.http import HttpResponseForbidden
from django.shortcuts import render
from functools import wraps

def AuthenticatedUser(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                return HttpResponseForbidden(render(request, "403.html", {"msg": "Please log in to access this page!"}))
            
            user_role = request.session.get('role')
            if user_role not in allowed_roles:
                return HttpResponseForbidden(render(request, "403.html", {"msg": "You do not have permission to access this page!"}))
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator