from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

def auth_action(detail=True, methods=None, permission_classes=None):
    if permission_classes is None:
        permission_classes = [IsAuthenticated]
    if methods is None:
        methods = ['post']

    return action(
        detail=detail,
        methods=methods,
        permission_classes=permission_classes
    )
