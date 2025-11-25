"""
Permisos y mixins personalizados para autorización por roles.
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from functools import wraps


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin para vistas basadas en clases: requiere usuario staff/admin."""
    def test_func(self):
        return self.request.user.is_staff


class OwnerRequiredMixin(UserPassesTestMixin):
    """Mixin para vistas basadas en clases: requiere ser dueño del objeto."""
    def test_func(self):
        obj = self.get_object()
        # Asume que el objeto tiene un campo 'user' o 'idUsuario'
        owner = getattr(obj, 'user', None) or getattr(obj, 'idUsuario', None)
        return owner == self.request.user


def admin_required(view_func):
    """Decorador para vistas basadas en funciones: requiere staff."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.user.is_staff:
            raise PermissionDenied("Acceso denegado: se requiere rol de administrador.")
        return view_func(request, *args, **kwargs)
    return wrapper


def owner_required(view_func):
    """Decorador para vistas basadas en funciones: requiere ser dueño del objeto."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        # La vista debe obtener el objeto y verificar ownership manualmente
        return view_func(request, *args, **kwargs)
    return wrapper
