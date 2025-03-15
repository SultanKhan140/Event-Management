from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """ Allow access only to Admins """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role_ref.id == 1

class IsOrganizer(BasePermission):
    """ Allow access only to Event Organizers """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role_ref.id == 2

class IsAttendee(BasePermission):
    """ Allow access only to Attendees """
    def has_permission(self, request, view):
        print("request.user.role_ref.id",request.user.role_ref.id)
        return request.user.is_authenticated and request.user.role_ref.id == 3
