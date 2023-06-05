from rest_framework import permissions
# EDIT THIS SHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIT
class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    '''
    Custom permissions for UserViewSet to edit their own profile.
    Otherwise, they can only create new users or see other people's profiles (GET and POST only).
    '''

		# Called when listing users:
    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_anonymous:
            return False
        else:
            return True
    
		# Called when accessing specific user instance:
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return request.user == obj
        
        return False