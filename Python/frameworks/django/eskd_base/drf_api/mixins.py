from rest_framework import permissions
from . import permissions as custom_permissions


class CustomMixin:
    permission_classes = [custom_permissions.IsOwnerOrReadOnly, permissions.IsAdminUser]