from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from stripe_cater.views import WebHookView

urlpatterns = [
    url(r'^webhooks/$', csrf_exempt(WebHookView.as_view()), name="invoice_list"),
]
