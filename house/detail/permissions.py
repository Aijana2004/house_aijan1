from rest_framework import permissions


class CheckAgencyCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'agency_owner':
            return True
        return False


class CheckOwnerAgency(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner


class CheckCompanyCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'company_owner':
            return True
        return False


class CheckOwnerCompany(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner


class CheckOwnerJK(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.company.owner


class CheckOwnerCreateApartment(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'owner':
            return True
        return False


class CheckOwnerApartment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner


class CheckAgencyApartment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.agency.owner



# class CheckOwnerAll(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return request.user == obj.owner and request.user == obj.owner
#
#


