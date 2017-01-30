from django.db.models.expressions import DateTime
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.views.generic.base import View
from base.model_invoice import Invoice, N_Invoice_Status, Proposal, N_Proposal_Status
from base.models import Business
from datetime import datetime

__author__ = 'Hector'

def Dashboard(request):

    #context = {'available_languages': ['en', 'es', 'fr']}
    user = request.user
    business = Business.objects.filter(owner=user).first()
    proximos_eventos = Invoice.objects.get_by_business(business=business).filter(proposal__event__event_date__gt = datetime.today()).order_by('proposal__event__event_date')

    proposals = Proposal.objects.get_by_business(business=business)
    proposals_aceptados = Proposal.objects.get_by_business(business=business).filter(status = N_Proposal_Status.ACCEPTED)
    proposal_porciento_ceptados = 0
    if len(proposals) > 0:
        proposal_porciento_ceptados = (len(proposals_aceptados) * 100) / len(proposals)


    past_due = Invoice.objects.filter(status=N_Invoice_Status.PAST_DUE)

    #TODO:Cambiar el estado y hacer la consulta apartir del dia primero del mes en curso
    ventas = Invoice.objects.get_by_business(business=business)

    total_ventas = sum([v.proposal.get_total() for v in ventas])

    context = {'proximos_eventos':proximos_eventos,'past_due':past_due,'ventas':ventas, 'total_ventas':total_ventas, 'proposals':proposals,'proposals_aceptados':proposals_aceptados, 'proposal_porciento_ceptados':proposal_porciento_ceptados}


    return render(request,'base/dashboard.html', context)

