from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View

__author__ = 'Hector'


class DashboardBeta(View):
    template_name = 'base_angular.html'

    def get(self, request, *args, **kwargs):

        return render_to_response(self.template_name, RequestContext(request))

class ErrorPage404(View):
    template_name = '404_error.html'

    def get(self, request, *args, **kwargs):

        return render_to_response(self.template_name, RequestContext(request))