import json
from django.core.urlresolvers import resolve, reverse
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View
from base.api.forms import BusinessProfileForm
from base.models import Business
from base.util import check_permission


class BusinessView(View):

    def get(self, request, *args, **kwargs):
        user  = request.user
        business = Business.objects.get_business_by_user(user=user)

        data = business.serialize()
        # print(resolve('login'))
        connect_stripe_url = reverse('connect_stripe',kwargs={'business_id':business.id})
        cancel_subcription_url = reverse('api_cancel_subcription')
        change_card_url = reverse('change_card')
        change_billing_email_url = reverse('api_change_billing_email')
        stripe_subscribe_url = reverse('stripe_subscribe')
        data['connect_stripe_url'] = connect_stripe_url
        data['cancel_subcription_url'] = cancel_subcription_url
        data['change_card_url'] = change_card_url
        data['change_billing_email_url'] = change_billing_email_url
        data['stripe_subscribe_url'] = stripe_subscribe_url


        return JsonResponse(data=data, safe=False)

    def _extract_data(self, data):
        owner = data.get('owner')
        address = data.get('address')

        profile_data = {}
        profile_data['phone'] = data.get('phone')
        profile_data['name'] = data.get('name')
        profile_data['tax'] = data.get('tax')
        profile_data['default_site'] = data.get('default_site_mine')
        profile_data['websiteurl'] = data.get('websiteurl')
        profile_data['capacity'] = data.get('capacity')

        profile_data['first_name'] = owner.get('first_name')
        profile_data['last_name'] = owner.get('last_name')
        profile_data['email'] = owner.get('email')

        profile_data['first_line'] = address.get('first_line')
        profile_data['second_line'] = address.get('second_line')
        profile_data['zip'] = address.get('zip')
        profile_data['city'] = address.get('city')
        profile_data['state'] = address.get('state').get('id')
        profile_data['country'] = address.get('country').get('id')

        return profile_data




    def post(self, request, *args, **kwargs):
        if not check_permission(request=request, permission='update_profile'):
            return HttpResponse(status=401)
        user  = request.user
        business = Business.objects.get_business_by_user(user=user)
        data = json.loads(request.body.decode())

        profile_data = self._extract_data(data=data)
        print('Es le usuario el que esta editado su profile:', user.email == profile_data.get('email'))

        # print(profile_data)

        form = BusinessProfileForm(profile_data)
        if form.is_valid():
            data_to_save = form.cleaned_data
            response = Business.objects.update_business_data(business=business, data=data_to_save)
            if response in Business.objects.ERRORS:
                if response == Business.objects.EMAIL_ERROR:
                    data = {'email':[{'code':'repeated', 'message':'Este correo ya esta en uso'}]}
                return JsonResponse(status=400, safe=False, data=json.JSONEncoder().encode(data))
            return HttpResponse(status=200)
        else:
            return JsonResponse(status=400, safe=False, data=form.errors.as_json())



class UploadLogoView(View):

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.FILES)
        logo = request.FILES.get('file')
        if logo:
            user  = request.user
            business = Business.objects.get_business_by_user(user=user)
            try:
                business.update_logo(logo)
                return JsonResponse(business.serialize(fields=['logo']), safe=False)
            except Exception as e:
                return HttpResponse(status=500)