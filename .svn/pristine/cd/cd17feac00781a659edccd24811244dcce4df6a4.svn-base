import json
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import View
from base.api.util import serialize_query
from base.model_invoice import Event
from base.models import Business


class EventView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.filter(owner=user).first()
        fields = Event.default_fields + ['proposal']
        if kwargs.get('id'):
            id = kwargs.get('id')

            event = Event.objects.get_event_by(id=id, business=business)

            if event in Event.objects.ERRORS:
                return HttpResponse(status=404)
            data = event.serialize(fields=fields)
        else:
            events = Event.objects.get_events_(business=business)

            data = serialize_query(events, fields=fields)

        return JsonResponse(safe=False, data=data)

class EventDeleteView(View):

    def post(self, request, *args, **kwargs):
        # if not check_permission(request=request, permission='delete_proposal'):
        #    return HttpResponse(status=401)
        user = request.user
        business = Business.objects.filter(owner=user).first()

        data = json.loads(request.body.decode())

        ids = [event.get('id') for event in data]
        try:
            deleted = Event.objects.bulk_delete(ids_list=ids)
            return JsonResponse(status=200, data={'deleted':deleted})
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
