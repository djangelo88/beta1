from django.contrib import admin

# Register your models here.
from django.contrib.admin.sites import site
from stripe_cater.models import StripeCustomer, StripeSubscripcion, PaymentOrder, Charge, StripeAccount, StripeInvoice, \
    StripeCard

site.register(StripeCustomer)
site.register(StripeSubscripcion)
site.register(PaymentOrder)
site.register(Charge)
site.register(StripeAccount)
site.register(StripeInvoice)
site.register(StripeCard)