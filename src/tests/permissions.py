from rest_framework.permissions import BasePermission


class IsUnsolved(BasePermission):
    """Allow access only to unsolved tests"""

    message = 'You have already solved this test'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or \
                request.user.solved_tests.filter(test_id=obj.id):
            return False
        return True


class IsOwner(BasePermission):
    """Allow access only if user is owner of object (and authenticated)"""

    message = 'You have already solved this test'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and obj.user == request.user:
            return True
        return False