from django.conf import settings
from business_site import site_url

__author__ = 'maykel'
import re


class SubdomainURLRoutingMiddleware(object):
    def process_request(self, request):
        domain = re.split(':', request.META['HTTP_HOST'])[0].lower()
        if not domain == settings.DEFAULT_SITE_DOMAIN:
            request.domain_name = domain
            request.urlconf = site_url
        return None
