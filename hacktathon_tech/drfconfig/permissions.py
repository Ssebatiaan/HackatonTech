from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
#from suscripcion.models import Cuenta


class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):
        return True


class AnonPermissionOnly(permissions.BasePermission):
    message = 'Tu te encuentras logueado'
    """
        Non-authenticated User only
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
