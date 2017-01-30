from django.conf import settings
from django.core.management.base import BaseCommand
from base.models import Business

__author__ = 'amado'
class Command(BaseCommand):

    def handle(self, *args, **options):
        list = Business.objects.get_customers_whose_trial_period_has_expired()
        for business in list:
            business.change_group(settings.BUSINESS_TRIAL, settings.BUSINESS_BASIC)