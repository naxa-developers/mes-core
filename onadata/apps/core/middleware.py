from onadata.apps.core.models import UserRole as Role
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render, redirect


def clear_roles(request):
    request.__class__.role = None
    request.__class__.project = None
    request.__class__.group = None
    request.__class__.is_super_admin = False
    return request


class RoleMiddleware(object):
    def process_request(self, request):
        if  'v1/forms/' in request.path_info:
            return None

        if request.META.get('HTTP_AUTHORIZATION'):
            token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            try:
                if request.user.is_anonymous():
                    request.user = Token.objects.get(key=token_key).user
            except:
                pass
        # print(request.user)
        if not request.user.is_anonymous():

            role = None
            if request.session.get('role'):
                try:
                    role = Role.objects.select_related('group', 'project').get(pk=request.session.get('role'),
                                                                                    user=request.user)
                except Role.DoesNotExist:
                    pass

            if not role:
                roles = Role.objects.filter(user=request.user).select_related('group', 'project')
                if roles:
                    role = roles[0]
                    request.session['role'] = role.id

            if role:
                request.__class__.role = role
                request.__class__.project = role.project

                if "super-admin" in request.user.user_roles.all().distinct('group__name').values_list('group__name',
                                                                                                      flat=True):
                    request.__class__.group = Group.objects.get(name="super-admin")
                    request.__class__.is_super_admin = True
                else:
                    request.__class__.group = role.group
                    request.__class__.is_super_admin = False
                return None
            else:
                request = clear_roles(request)
                logout(request)
                return render(request, '403.html')

        else:
            request = clear_roles(request)

