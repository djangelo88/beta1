from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import views

from base.models import ConfirmEmailOrder


def password_change_done(request):
    return HttpResponse(content="Your Password has changed");

def password_change(request):
    if request.method == 'GET' or not request.is_ajax():
        template_response = views.password_change(request, template_name='base/password_change.html')
        return template_response
    else:
        print('ajax')
        template_response = views.password_change(request, template_name='base/password_change_partial.html')
        return template_response

def password_reset(request):
    if request.method == 'GET' or not request.is_ajax():
        template_response = views.password_reset(request, from_email=settings.ADMIN_EMAIL, template_name='base/password_reset.html')
        return template_response
    else:
        print('ajax')
        template_response = views.password_reset(request, template_name='base/password_reset.html')
        return template_response

def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == 'GET' or not request.is_ajax():
        template_response = views.password_reset_confirm(request, uidb64=uidb64, token=token,template_name='base/password_reset_confirm.html')
        return template_response
    else:
        print('ajax')
        template_response = views.password_reset_confirm(request, template_name='base/password_reset_confirm.html')
        return template_response

class ConfirmEmailView(View):

    def get(self, request, *args, **kwargs):
      uidb64 = kwargs.get('uidb64')
      token = kwargs.get('token')

      order = ConfirmEmailOrder.objects.filter(key=uidb64).filter(checked=False).first()
      if order and default_token_generator.check_token(order.user, token):
          response = order.invoke()
          if response == ConfirmEmailOrder.OK:
              return HttpResponseRedirect(redirect_to=reverse('login'))
          else:
            error = 'Error'
            if response == ConfirmEmailOrder.EMAIL_ERROR:
                error = 'Correo Repetido'
            if response == ConfirmEmailOrder.EXPIRED:
                error = "Too Late"
            return HttpResponse(status=400,content=error)
      else:
          return HttpResponse(status=404)

