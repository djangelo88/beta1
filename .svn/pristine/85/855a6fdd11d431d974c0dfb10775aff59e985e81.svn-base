from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

__author__ = 'amado'

def check_permission(request, permission, app_label='base'):
    permission_name = app_label + '.' + permission
    return request.user.has_perm(permission_name)

