from django.conf import settings

__author__ = 'maykel'
from django.conf.urls import patterns, include, url, static
from business_site.views import WebsiteRender, SendMailContact

urlpatterns = [
                  url(r'^$', WebsiteRender, name='r'),
                  url(r'^sendmailcontact/$', SendMailContact.as_view(), name='sendmailcontact')
              ] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)