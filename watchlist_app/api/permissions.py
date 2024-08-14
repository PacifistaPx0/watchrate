from rest_framework import permissions

class ReviewUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:   # Only allow owners to update or delete their own objects
            return obj.review_user == request.user
