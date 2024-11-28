from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(allowed_roles):
    """
    Decorators to restrict access to views based on the roles
    """
    
    def decorator(view_func):
        @login_required(login_url="users:user_login")
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'role') and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect("users:user_login")
        return _wrapped_view
    return decorator