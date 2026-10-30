from rest_framework.permissions import BasePermission

class IsAdministrator(BasePermission):

    def has_permission(self, request, view):

        return(
            request.user.is_authenticated and 
            request.user.groups.filter
            (name = "Administrador").exists()
        )

class CanManageStock(BasePermission):

    def has_permission(self, request, view):

        return(
            request.user.is_authenticated and 
            request.user.has_perm
            ("inventory.add_stockmovement")
        )

class CanViewStock(BasePermission):

    def has_permission(self, request, view):

        return(
            request.user.is_authenticated and
            request.user.has_perm
            ("inventory.view_stockmovement")
        )