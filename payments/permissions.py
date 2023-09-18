from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin or the owner of the payment
        return request.user.is_staff or obj.borrowing.user == request.user
