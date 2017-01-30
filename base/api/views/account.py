from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View
from django.contrib.auth import views, update_session_auth_hash
import json
from base.forms import BillingEmailForm
from base.models import Business
from stripe_cater.services import update_billing_email



class ChangePassword(View):

    def post(self, request, *args, **kwargs):
        print(request.body)
        data = json.loads(request.body.decode())
        form = PasswordChangeForm(user=request.user, data=data)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponse()
        else:
            errors = (form.errors.as_json())
            return JsonResponse(safe=False, data=errors, status=400)

        return HttpResponse(content='Hello')


