from functools import wraps
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from api.text import PERMISSION_DENIED_MUST_AUTH


def is_authenticated_only(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        if not IsAuthenticated().has_permission(request, self):
            raise PermissionDenied(PERMISSION_DENIED_MUST_AUTH)
        return func(self, request, *args, **kwargs)
    return wrapped
