from django.core.urlresolvers import reverse
from django.http.response import HttpResponse

__author__ = 'amado'

def has_permission(view_fun, permission):
    print(permission)
    def wrapper(*args, **kwargs):
        print("Jamon")
        request = args[0]
        user = request.user
        print(user.has_perm(permission))
        if not user.has_perm(permission):
            return HttpResponse(reverse('login'))

        return view_fun(*args, **kwargs)

    return wrapper


