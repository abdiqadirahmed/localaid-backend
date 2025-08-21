from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsDonorOrReadOnly(BasePermission):
    """
    Allow only the donor who created the resource to edit/delete it.
    Anyone can read.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only permissions for GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only for the original donor
        return obj.donor == request.user
