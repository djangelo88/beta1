from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View
from base.api.util import serialize_query
from base.model_invoice import N_Request_Type, N_Event_Status, N_Invoice_Status, N_Proposal_Status, Proposal, Event, \
    Invoice
from base.models import N_Prefix, N_Suffix, Customer, N_Company, N_Country
from base.prodserv_models import Measure, Magnitude, Conversion, Product, Service

NOMENCLATOR_CLASS = {'request':N_Request_Type, 'event_status':N_Event_Status,
                     'invoice_status':N_Invoice_Status, 'proposal_status':N_Proposal_Status,
                        'prefix': N_Prefix, 'suffix':N_Suffix,'company':N_Company,
                        'country':N_Country,'magnitude':Magnitude,'measure':Measure,
                     'conversion':Conversion,'product':Product, 'service':Service
                         }

class Nomenclator(View):

    def get(self, request, *args, **kwargs):
        model_key = (request.GET.get('model'))
        id = (request.GET.get('id'))
        print(model_key)
        model_id = (request.GET.get('id'))
        model = NOMENCLATOR_CLASS.get(model_key)
        # if model and model_id:
        #     respones = model.objects.get(id = model_id)
        #     return JsonResponse(safe=False, data=respones)
        # try:
        if model:
            if id:
                response = model.objects.get(pk=id)
                respones = response.serialize()
            else:
                # respones = list(model.objects.all().values())
                respones = serialize_query(query_set=model.objects.all())
            return JsonResponse(safe=False, data=respones)
        return HttpResponse(status=400)
        # except Exception as e:
        #     print(e)
        #     return HttpResponse(status=400)

class Country(View):

    def get(self, request, *args, **kwargs):
        pass