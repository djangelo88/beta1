from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from base.decorators import has_permission

from base.forms import BusinessForm, BusinessProfileForm
from base.models import Business, ConfirmEmailOrder
from base.tasks import task_sendmail_confirm_registration, start_thread
from base.util import check_permission
from stripe_cater import services
from stripe_cater.exceptions import StripeException
from stripe_cater.services import initial_subscribe_bussines


class BusinessRegister(View):
   # def get(self, request, *args, **kwargs):
   #     form = BusinessForm()
   #     return render_to_response("base/business/business.html", RequestContext(request, {'form':form}))

   def get(self, request, *args, **kwargs):
       form = BusinessForm()
       return render_to_response("base/business/business.html", RequestContext(request, {'form':form}))

   # def get(self, request, *args, **kwargs):
   #     form = BusinessForm()
   #     PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY
   #     return render_to_response("base/business/business.html", RequestContext(request, {'form':form,
   #                                                                                       'PUBLISHABLE_KEY':
   #                                                                                       PUBLISHABLE_KEY}))

   def post(self, request, *args, **kwargs):

       form = BusinessForm(request.POST)
       errors = {}
       email_error = ''
       if form.is_valid():
           response = Business.objects.create_business(form.cleaned_data)
           if response not in Business.objects.ERRORS:
               business = response
               user = business.owner
               email_order = ConfirmEmailOrder.objects.create_confirm_register_email(user)
               # task_sendmail_confirm_registration(order)
               start_thread(task_sendmail_confirm_registration, email_order)
               return HttpResponseRedirect(redirect_to=reverse('login'))
           else:
               if response == Business.objects.EMAIL_ERROR:
                   email_error = 'Correo en uso, por favor especifique uno nuevo'
               else:
                   errors = 'Error al procesar su peticion. Intente de nuevo'
               print(response)
               return render_to_response('base/business/business.html', RequestContext(request,{'form':form,'errors':errors,'email_error':email_error}))
       else:

           return render_to_response('base/business/business.html', RequestContext(request,{'form':form,'errors':errors}))

   # def post(self, request, *args, **kwargs):
   #
   #         form = BusinessForm(request.POST)
   #         errors = {}
   #         if form.is_valid():
   #             try:
   #                 with transaction.atomic():
   #                     business = Business.objects.create_business(form.cleaned_data)
   #                     stripeToken = request.POST.get('stripeToken')
   #                     response = initial_subscribe_bussines(token=stripeToken, business=business)
   #
   #                     business.set_stripe_customer(customer=response)
   #                     user = business.owner
   #                     email_order = ConfirmEmailOrder.objects.create_confirm_register_email(user)
   #                     start_thread(task_sendmail_confirm_registration, email_order)
   #                     return HttpResponseRedirect(redirect_to=reverse('login'))
   #             except ValidationError:
   #                 errors = 'Correo en Uso'
   #             except StripeException:
   #                 errors = 'Error en los datos de su cuenta para subscribirlo a stripe'
   #             except Exception:
   #                 errors = 'Error al procesar su peticion. Intente de nuevo'
   #             # if response not in Business.objects.ERRORS:
   #             #
   #             #     business = response
   #             #     user = business.owner
   #             #     email_order = ConfirmEmailOrder.objects.create_confirm_register_email(user)
   #             #     # task_sendmail_confirm_registration(order)
   #             #     start_thread(task_sendmail_confirm_registration, email_order)
   #             #     return HttpResponseRedirect(redirect_to=reverse('login'))
   #             # else:
   #             #     print(response)
   #             return render_to_response('base/business/business.html', RequestContext(request,{'form':form,'errors':errors}))
   #         else:
   #
   #             return render_to_response('base/business/business.html', RequestContext(request,{'form':form,'errors':errors}))


class BusinessProfile(View):

   def set_data_from_business(self, business):
       data = {}
       data['name'] = business.name
       data['address'] = business.address
       data['phone'] = business.phone
       data['tax'] = business.tax
       owner = business.owner
       data['email'] = owner.email
       data['first_name'] = owner.first_name
       data['last_name'] = owner.last_name
       data['websiteurl'] = business.websiteurl
       data['default_site'] = business.default_site_mine
       return data


   def get(self, request, *args, **kwargs):
       user = request.user
       business = Business.objects.filter(owner=user).first()
       # need_payment = business.need_payment_order()
       initial = self.set_data_from_business(business)
       form = BusinessProfileForm(initial=initial)

       subscription = business.get_subscription()

       if business.logo:
           logo_url = business.logo.url[business.logo.url.find('/media/'+settings.PROFILE_DIR_NAME+'/'):]
       else:
           logo_url = None

       return render_to_response("base/business/profile.html", RequestContext(request, {'logo_url':logo_url,'business':business,'form':form, 'subscription':subscription,
                                                                                                           }))




   def post(self, request, *args, **kwargs):
        if not check_permission(request=request, permission='update_profile'):
           return HttpResponseRedirect(redirect_to=reverse('login'))

        is_ajax = request.is_ajax()

        user = request.user
        business = Business.objects.filter(owner=user).first()
        logo_url = business.get_logo_url


        # need_payment = business.need_payment_order()
        # logo_url = business.logo.url[business.logo.url.find('/media/'+settings.PROFILE_DIR_NAME+'/'):]
        form = BusinessProfileForm(request.POST, request.FILES)
        errors = {}
        if form.is_valid():

            response = Business.objects.update_business_data(business, form.cleaned_data, logo=request.FILES.get('logo'))

                
            if response in Business.objects.ERRORS:
                if response == Business.objects.EMAIL_ERROR:
                    errors['email'] = "Correo Repetido"
                if is_ajax:
                    return JsonResponse([errors, form.errors], status=400)
                print(errors)
                print(response)
                return render_to_response("base/business/profile.html", RequestContext(request, {'logo_url':logo_url,'business':business,'form':form,'errors':errors}))
            else:
                logo_url = response.get_logo_url
                if is_ajax:
                    return HttpResponse()
                return HttpResponseRedirect(redirect_to=reverse('dashboard'))
                #return render_to_response("base/business/profile.html", RequestContext(request, {'logo_url':logo_url,'business':business,'form':form}))
        else:
            if is_ajax:
                    return JsonResponse(form.errors,status=400)
            return render_to_response("base/business/profile.html", RequestContext(request, {'logo_url':logo_url,'business':business,'form':form,'errors':errors}))

# class PaymentOrder(View):
#
#     def post(self, request, *args, **kwargs):
#         is_ajax = request.is_ajax()
#
#         user = request.user
#         business = Business.objects.filter(owner=user).first()
#         need_payment = business.need_payment_order()
#
#         if not need_payment:
#             return HttpResponse(status=400)
#         response = business.get_subscription().create_payment_order()
#         if response in Subscription.ERRORS:
#             if is_ajax:
#                 return JsonResponse(response)
#             else:
#                 return HttpResponse(content=response)
#         else:
#             if is_ajax:
#                 return JsonResponse(response.id)
#             else:
#                 return HttpResponse(content=response.id)

