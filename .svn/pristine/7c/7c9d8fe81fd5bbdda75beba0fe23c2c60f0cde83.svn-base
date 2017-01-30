import json

from django.conf import settings
from django.http.response import HttpResponse


# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import stripe
from stripe_cater.models import EventRecord
from stripe_cater.services import customer_subscription_updated, customer_subscription_trial_will_end, \
    customer_subscription_deleted, invoice_created, invoice_payment_succeeded, invoice_payment_failed


class WebHookView(View):
    def get_callback(self, type):
        if type == 'customer.subscription.updated':
            return customer_subscription_updated
        elif type == 'customer.subscription.trial_will_end':
            return customer_subscription_trial_will_end
        elif type == 'customer.subscription.deleted':
            return customer_subscription_deleted
        elif type == 'invoice.created':
            return invoice_created
        elif type == 'invoice.payment_succeeded':
            return invoice_payment_succeeded
        elif type == 'invoice.payment_failed':
            return invoice_payment_failed

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY

        event_json = json.loads(request.body.decode())

        # Verify the event by fetching it from Stripe
        event = stripe.Event.retrieve(event_json["id"])
        try:
            # record = EventRecord.objects.filter(stripeid=event_json["id"]).first()
            record = EventRecord.objects.filter(stripeid=event.id).first()
            if record:
                pass
            else:
                callback = self.get_callback(event_json["type"])
                callback(event_json)
                EventRecord.objects.create(event_json["id"])
        except:
            pass


            # Do something with event

        return HttpResponse(status=200)