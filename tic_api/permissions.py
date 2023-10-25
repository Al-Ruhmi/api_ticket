from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):

        # if request.user.is_staff:

        return request.user.is_authenticated and request.user.is_staff == True
        

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):

        # if request.user.is_staff is None:

        return request.user.is_authenticated and request.user.is_staff == False