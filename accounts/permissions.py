from rest_framework.permissions import BasePermission
from rest_framework import permissions



class IsRequester(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'requester'

class IsDonor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'donor'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

