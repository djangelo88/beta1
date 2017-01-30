from datetime import timedelta
import json
from django.db import transaction
from django.shortcuts import render_to_response
from django.utils import formats
from django.db.models.fields import DateTimeField
from django.http.response import JsonResponse, HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import View
from base.api.util import serialize_query
from base.model_invoice import Proposal, Event
from base.models import Business, N_State
from base.api.forms import EventForm
from base.tasks import start_thread, task_send_proposal, OK
from base.util import check_permission

__author__ = 'amado'

class ProposalView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()

        if kwargs.get('id'):
            id = kwargs.get('id')

            prop = Proposal.objects.get_by_id(id=id, business=business)
            print(prop)
            if prop in Proposal.objects.ERRORS:
                return HttpResponse(status=404)
            data = prop.serialize()
        else:
            proposal = Proposal.objects.get_by_business(business=business)

            data = serialize_query(proposal)

        return JsonResponse(safe=False, data=data)

    def prepre_data(self, data):
        result = {}
        evento = data.get('event')
        address = evento.get('address')
        customer = evento.get('customer')
        event_data = {}
        event_data['name'] = evento.get('name')
        event_data['customer'] = customer.get('id')
        event_data['comments'] = data.get('comments')
        event_data['first_line'] = address.get('first_line')
        event_data['second_line'] = address.get('second_line')
        event_data['zip'] = address.get('zip')
        event_data['city'] = address.get('city')
        event_data['city'] = address.get('city')
        event_data['state'] = address.get('state').get('id')
        # print(evento.get('event_date'))
        event_date = DateTimeField().to_python(evento.get('event_date')).date()
        event_date = DateTimeField().to_python(event_date.isoformat())
        event_time = DateTimeField().to_python(evento.get('event_time'))
        delta = timedelta(hours=event_time.hour, minutes=event_time.minute)
        print(event_date)
        event_date = event_date + delta
        event_data['event_date'] = formats.date_format(event_date, 'Y-m-d H:m')
        result['event_data'] = event_data
        result['address'] = address
        return result

    def post(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()
        data = json.loads(request.body.decode())
        send = data.get('send')
        prepared_data = self.prepre_data(data=data)
        event_data = prepared_data['event_data']
        # print(event_data)
        items = data.get('items')

        eventform = EventForm(event_data)
        if eventform.is_valid():
            # print(eventform.cleaned_data)
            # respones = Event.objects.create_or_update_event(data=eventform.cleaned_data)
            try:
                with transaction.atomic():
                    proposal = None
                    if data.get('id'):
                        id = data.get('id')
                        proposal = Proposal.objects.get_by_id(id=id, business=business)

                    response = Event.objects.create_or_update_proposal_from_event(data=eventform.cleaned_data, proposal=proposal)
                    if response in Event.objects.ERRORS:
                        raise RuntimeError()
                    print(items)
                    response.add_items_list(items)
                    if send:
                        old_status = response.status
                        response.prepare_to_send()
                        start_thread(task_send_proposal, response, old_status)
                    return JsonResponse(data=response.serialize(), safe=False)
            except Exception as e:
                print(e)
                return JsonResponse(data={'global':[{'message':'Lo sentimos'}]},status=400, safe=False)
        else:
            print(eventform.errors.as_json())
            print('meti la pata')
            return JsonResponse(data=eventform.errors.as_json(),status=400, safe=False)


class ProposalDeleteView(View):

    def post(self, request, *args, **kwargs):
        if not check_permission(request=request, permission='delete_proposal'):
           return HttpResponse(status=401)
        user = request.user
        business = Business.objects.filter(owner=user).first()

        data = json.loads(request.body.decode())

        ids = [prop.get('id') for prop in data]
        try:
            deleted = Proposal.objects.bulk_delete(ids_list=ids, business=business)
            return JsonResponse(status=200, data={'deleted':deleted})
        except Exception as e:
            print(e)
            return HttpResponse(status=400)

class ProposalEmailSend(View):

    def post(self, request, *arg, **kwargs):
        if not check_permission(request=request, permission='mail_proposal'):
                return HttpResponse(status=401)
        id = kwargs.get('id')

        user = request.user
        business = Business.objects.get_business_by_user(user=user)

        proposal = Proposal.objects.get_by_id(id=id, business=business)
        proposal.event.accepted()
        if proposal in Proposal.objects.ERRORS or not proposal.may_send_email():
            return HttpResponse(status=404)

        old_status = proposal.status
        proposal.prepare_to_send()
        response = task_send_proposal(proposal, old_status=old_status)

        if response == OK:
            return JsonResponse(status=200, data=proposal.serialize(), safe=False)
        else:
            return JsonResponse(status=500, data={})

class ProposalDeny(View):

    def get(self, request, *args, **kwargs):
        pidb64 = kwargs.get('pidb64')
        tokenb64 = kwargs.get('token')
        id = kwargs.get('id')
        if id:
            if not check_permission(request=request, permission='deny_proposal'):
                return HttpResponse(status=401)
            user = request.user
            business = Business.objects.get_business_by_user(user=user)

            proposal = Proposal.objects.get_by_id(id=id, business=business)

            if proposal in Proposal.objects.ERRORS:
                return HttpResponse(status=404)
            response = proposal.deny_by_business();

            if response in Proposal.ERRORS:
                return JsonResponse(data={'error':response},status=400)
            return JsonResponse(data=response.serialize())
        try:
            id = force_text(urlsafe_base64_decode(pidb64))
            token = force_text(urlsafe_base64_decode(tokenb64))

            response = Proposal.objects.deny_proposal(id=id, token=token)
            print(response)
            if response == Proposal.objects.ERROR_TOKEN:
                return render_to_response("base/invoice/proposal/failed.html")
            elif response == Proposal.objects.ERROR_EXPIRED:
                return render_to_response("base/invoice/proposal/failed.html")
            else:
                return render_to_response("base/invoice/proposal/denied_success.html")
        except Exception as e:
            print(e)
            return HttpResponse(status=400)