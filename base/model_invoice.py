from datetime import datetime

from django.db import models, transaction


#Managers
from django.db.models.aggregates import Count
from django.db.models.fields import DateTimeField
from django.utils import formats
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from base.api.util import serialize_query
from base.exceptions import EventDataError
from base.prodserv_models import Product, Service
from base.signals import proposal_accepted, event_booking_success
from stripe_cater.models import PaymentOrder


class EventManager(models.Manager):
    ERROR = -1
    ERRORS = [ERROR]
    def get_event_by(self, id, business=None):
        query = self.exclude(status=N_Event_Status.CANCELLED).filter(id=id)
        if business:
            query = query.filter(customer__business=business)
        return query.first()

    def create_or_update_invoice_from_event(self, data, invoice, handly = False):

        if invoice:
            response = self.create_or_update_proposal_from_event(data, proposal=invoice.proposal)
            if response in self.ERRORS:
                return response
            else:
                invoice.status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.EDITTING)
                invoice.update_due_date(data.get('due_date'))
                # changing_event_data.send(sender=Invoice,invoice=invoice)
                return invoice
        else:
           response = self.create_or_update_proposal_from_event(data, from_invoice= handly)
           if response in self.ERRORS:
                return response
           else:
                response = Invoice.objects.create_from_proposal(due_date=data.get('due_date'),proposal=response)
                if response in Invoice.objects.ERRORS:
                    return self.ERROR
                else:
                    return response

    def create_or_update_proposal_from_event(self, data, proposal=None, from_invoice=False):
        comment = data.get('comment')
        if proposal:
            response = self.create_or_update_event(data=data, instance=proposal.event)
            if response not in self.ERRORS:
                if proposal.status.id != N_Proposal_Status.DENIED:#para que se mantenga denegado
                    proposal.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.EDITTING)
                proposal.client_message = comment
                proposal.save()
                # changing_event_data.send(sender=Proposal,proposal=proposal)
                return proposal
            else:
                return response
        else:

            response = self.create_or_update_event(data=data,status=N_Event_Status.ACCEPTED)
            if response in self.ERRORS:
                return response


            try:
               proposal =  Proposal.objects.create_proposal(event=response,client_message=comment, from_invoice=from_invoice)
               return proposal
            except Exception as e:
                print(e)
                return self.ERROR


    def create_or_update_event(self, data, instance=None, status=None):
        name = data.get('name')
        # address = data.get('address')
        event_date = data.get('event_date')
        # due_date = data.get('due_date')
        customer = data.get('customer')
        address = {}
        address['first_line'] = data.get('first_line')
        address['second_line'] = data.get('second_line')
        address['zip'] = data.get('zip')
        address['city'] = data.get('city')
        address['state'] = data.get('state')

        try:
            if instance:
                instance.name = name
                instance.address.update(data=address)
                instance.event_date = event_date
                # instance.due_date = due_date
                instance.customer = customer

                instance.save()

                return instance
            else:
                status_value = N_Event_Status.objects.get(pk=N_Event_Status.ACCEPTED)
                if status:
                    status_value = status
                address_obj = Address.objects.create_address(data=address)

                event = self.create(name=name, address=address_obj, event_date = event_date,
                                    # due_date=due_date,
                                    customer=customer, status=status_value)

                return event
        except Exception as e:
            print(e)
            return self.ERROR

    def create_event_from_external_source(self, data, customer, req_platos=[], req_servicios=[]):
        data_to_save = {'name':data.get('evento_name'),
                        'address':data.get('evento_address'),
                        'event_date':data.get('evento_date'),
                        'customer':customer,
                        'first_line': data.get('evento_first_line'),
                        'second_line': data.get('evento_second_line'),
                        'city':data.get('evento_city'),
                        'zip':data.get('evento_zip'),
                        'state':data.get('evento_state')
                        }


        business = customer.business

        param_event_date = DateTimeField().to_python(value=data.get('evento_date'))
        schedule_events_at = self.number_of_events_schedule_at(event_date=param_event_date.date(),
                                                               business=business)


        can_be_accepted = business.can_accepted_one_more(schedule_events_at)

        status = N_Event_Status.objects.get(pk=N_Event_Status.PENDING)

        if can_be_accepted:
            status = N_Event_Status.objects.get(pk=N_Event_Status.ACCEPTED)

        print(can_be_accepted)
        response = self.create_or_update_event(data=data_to_save, status=status)

        if response in self.ERRORS:
            raise EventDataError()
        # asociar casa req al evento
        type = N_Request_Type.objects.get(pk=N_Request_Type.PRODUCT)
        requests = []
        for req in req_platos:
            req_obj = Request.objects.create_from_external_source(data=req, event=response, type=type)
            requests.append(req_obj)
        type = N_Request_Type.objects.get(pk=N_Request_Type.SERVICE)
        for req in req_servicios:
            req_obj = Request.objects.create_from_external_source(data=req, event=response, type=type)
            requests.append(req_obj)
        print(requests)
        Request.objects.bulk_create(requests)


        event_booking_success.send(sender=None,event=response)
        return response



    def number_of_events_schedule_at(self, event_date, business):
        return self.filter(customer__business=business).filter(event_date__date=event_date).exclude(status=N_Event_Status.CANCELLED).count()

    def get_events_(self, business=None, id=None):
        query = self.exclude(status=N_Event_Status.CANCELLED)
        if id:
            query = query.filter(id=id)
        if business:
          query = query.filter(customer__business=business)
        return query

    def bulk_delete(self, ids_list):
        status = N_Event_Status.objects.get(pk=N_Event_Status.CANCELLED)
        with transaction.atomic():
            Invoice.objects.bulk_delete_by_events(event_ids_list=ids_list)
            Proposal.objects.bulk_delete_by_evetns(event_ids_list=ids_list)
            deleted = self.filter(id__in=ids_list).update(status=status)
            return deleted

class ProposalManager(models.Manager):
    ERROR = -1
    ERROR_TOKEN = -2
    ERROR_EXPIRED = -3
    ERROR_INVOICE = -4
    ERROR_PRESUPUESTO_ACCEPTADO =-5
    ERROR_PRESUPUESTO_DENEGADO= -6
    OK = 0
    ERRORS = [ERROR, ERROR_TOKEN,ERROR_EXPIRED]
    def generate_number(self):
        return int(datetime.today().timestamp() * 1000000)
    def create_proposal(self, event, client_message=None, from_invoice=False):
        status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.EDITTING)
        if from_invoice:
            status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
        return self.create(event=event, status=status, number=self.generate_number(), client_message=client_message)
    def create_proposal_from_external_source(self, event):
        return self.create_proposal(event=event)

    def get_by_id(self, id, business=None, hide_cancelled=True):
        query = self.filter(id=id)
        if hide_cancelled:
          query = query.exclude(status=N_Proposal_Status.CANCELLED)
        if business:
            query = query.filter(event__customer__business=business)
        p = query.first()
        if p:
            return p
        else:
            return self.ERROR

    def get_by_business(self, business, hide_cancelled=True):
        query = self.filter(event__customer__business=business)
        if hide_cancelled:
           query =  query.exclude(status=N_Proposal_Status.CANCELLED)
        return query



    def deny_proposal(self, id, token):
        p = self.filter(id=id).filter(send_token=token).filter(status=N_Proposal_Status.PENDING).first()
        if p:
            if p.has_expired():
                return self.ERROR_EXPIRED
            p.deny()
            # p.reset_token()
            # p.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.DENIED)
            # p.save()
            return p
        else:
            return self.ERROR_TOKEN

    def accpet_proposal(self, id, token):
        p = self.filter(id=id).filter(send_token=token).filter(status=N_Proposal_Status.PENDING).first()
        if p:
            if p.has_expired():
                return self.ERROR_EXPIRED
            response = p.accept()

            if response in Invoice.objects.ERRORS:
                return self.ERROR_INVOICE
            # p.reset_token()
            # p.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
            # p.save()
            return p
        else:
            return self.ERROR_TOKEN

    def cancell_proposal(self, proposal):
        try:
            proposal.status = N_Proposal_Status.objects.get(id=N_Proposal_Status.CANCELLED)
            proposal.save()
            return self.OK
        except:
            return self.ERROR

    def bulk_delete(self, ids_list, business):
        cancelled_status = N_Proposal_Status.objects.get(id=N_Proposal_Status.CANCELLED)
        Proposal.objects.filter(id__in=ids_list).filter(event__customer__business=business).update(status=cancelled_status)

    def bulk_delete_by_evetns(self, event_ids_list):
        cancelled_status = N_Proposal_Status.objects.get(id=N_Proposal_Status.CANCELLED)
        Proposal.objects.filter(event__id__in=event_ids_list).update(status=cancelled_status)

    def get_invoices_all(self, business):
        return  self.annotate(ni=Count('invoice')).filter(ni=1).\
                filter(event__customer__business=business).filter(invoice__deleted=False)

class InvoiceManager(models.Manager):
    ERROR = -1
    ERROR_TOKEN = -2
    ERROR_EXPIRED = -3
    OK = 0
    ERRORS = [ERROR, ERROR_EXPIRED, ERROR_TOKEN]
    def generate_number(self):
        return str(int(datetime.today().timestamp() * 1000000))

    def create_from_proposal(self, proposal, handly = True, due_date=None):
        try:
            # status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.CREATED)
            # if handly:
            status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.EDITTING)

            due_date_value = proposal.event.event_date
            if due_date:
                due_date_value = due_date

            invoice = self.create(due_date=due_date_value,
                number=self.generate_number(), proposal=proposal, status=status)
            return invoice
        except Exception as e:
            print(e)
            return self.ERROR

    def get_by_id(self, id, business=None, hide_deleted=True):
        query = self.filter(id=id)
        if hide_deleted:
          query = query.exclude(deleted=True)
        if business:
            query = query.filter(proposal__event__customer__business=business)
        inv = query.first()
        if inv:
            return inv
        else:
            return self.ERROR

    def get_invoice_to_pay_by_id(self, id, token):
        invoice = self.filter(id=id).exclude(deleted=True).filter(send_token=token).first()
        print(invoice.status)
        if invoice and invoice.status.id not in [N_Invoice_Status.PAID]:
            return invoice
        else:
            return self.ERROR


    def get_by_business(self, business, hide_deleted=True):
        query = self.filter(proposal__event__customer__business=business)
        if hide_deleted:
           query = query.exclude(deleted=True)
        return query



    def delete_invoice(self, invoice):
        response = Proposal.objects.cancell_proposal(invoice.proposal)
        if response in Proposal.ERRORS:
            return self.ERROR
        try:
            invoice.deleted = True
            invoice.save()
            return self.OK
        except:
            return self.ERROR

    def get_invoice_by_payment(self, payment):
        return self.filter(payment_order=payment).first()

    def get_by_proposal(self, proposal):
        return self.filter(proposal=proposal).first()

    def chekc_due_date(self, business=None):
        today = datetime.today()
        query = Invoice.objects.filter(status=N_Invoice_Status.PENDING).filter(due_date__lt=today)
        if business:
            query = query.filter(proposal__event__customer__business=business)
        query.update(status=N_Invoice_Status.PAST_DUE)

    def bulk_delete(self, ids_list, business):
        Invoice.objects.filter(id__in=ids_list).filter(proposal__event__customer__business=business).update(deleted=True)

    def bulk_delete_by_events(self, event_ids_list):
        Invoice.objects.filter(proposal__event__id__in=event_ids_list).update(deleted=True)


class ItemManager(models.Manager):
     ERROR = -1
     ERRORS = [ERROR]
     def update_item(self, data, item):
          try:
              oferta = data.get('oferta')
              oferta = Oferta.objects.get_oferta_by_name(name=oferta, business=item.oferta.business)
              discount = data.get('discount')
              unit_cost = data.get('unit_cost')
              quantity = data.get('quantity')
              tax = data.get('tax') or item.proposal.get_tax()
              description = data.get('description')

              item.tax = tax
              item.oferta = oferta
              item.discount = discount
              item.description = description
              item.unit_cost = unit_cost
              item.quantity = quantity

              item.save()
              # changing_item_data.send(sender=None, proposal=item.proposal)
              return item
          except:
              return self.ERROR

     def delete_item(self,id):
         try:
            item = self.get(pk=id)
            # changing_item_data.send(sender=None, proposal=item.proposal)
            item.delete()
         except Exception as e:
             print(e)
             pass

     def create_item(self, item_data,proposal, flush=True):
         type_id = item_data.get('type')
         if isinstance(type_id, dict):
             type_id = type_id.get('id')
         type = N_Request_Type.objects.get(pk=type_id)

         item_entity = Item(proposal=proposal,
                                   tax=item_data.get('tax'),
                                   discount=item_data.get('discount'),
                                   unit_cost=item_data.get('unit_cost'),
                                   quantity=item_data.get('quantity'),
                                   type=type,
                                   )
         request_id = item_data.get('request')
         if isinstance(request_id, dict):
             request_id = request_id.get('id')

         if type.id == N_Request_Type.PRODUCT:
             item_entity.product = Product.objects.get(pk=request_id)
         else:
             item_entity.service = Service.objects.get(pk=request_id)

         if flush:
             item_entity.save()

         return item_entity

     def update_item(self, item_data,flush=True):
         item = self.get(pk=item_data.get('id'))

         type_id = item_data.get('type')
         if isinstance(type_id, dict):
             type_id = type_id.get('id')

         type = N_Request_Type.objects.get(pk=type_id)
         item.tax=item_data.get('tax')
         item.discount=item_data.get('discount')
         item.unit_cost=item_data.get('unit_cost')
         item.quantity=item_data.get('quantity')
         item.type = type


         if type.id == N_Request_Type.PRODUCT:
             item.product = Product.objects.get(pk=item_data.get('product').get('id'))
         else:
             item.service = Service.objects.get(pk=item_data.get('service').get('id'))

         if flush:
             item.save()

         return item


class RequestManager(models.Manager):

    def create_from_external_source(self, type,event, data, flush=False):

        req = Request(type=type, event=event, amount=data.get('amount'))
        if type.id == N_Request_Type.PRODUCT:
            req.product = Product.objects.get(pk=data.get('id'))
        else:
            req.service = Service.objects.get(pk=data.get('id'))

        if flush:
            req.save()
        return req

#Models
from base.models import Customer, Oferta, ModelSerialize, Address


class Event(models.Model, ModelSerialize):
    objects = EventManager()
    name = models.CharField(max_length=255)
    # address = models.CharField(max_length=255)
    address = models.ForeignKey(Address)
    event_date = models.DateTimeField()
    # due_date = models.DateField()
    customer = models.ForeignKey(Customer)
    status = models.ForeignKey('N_Event_Status')

    default_fields = ['name','address','event_date','customer','status','id','can_remove']

    def schedule(self):
        self.status = N_Event_Status.objects.get(pk=N_Event_Status.SCHEDULED)
        self.save()

    def accepted(self):
        self.status = N_Event_Status.objects.get(pk=N_Event_Status.ACCEPTED)
        self.save()

    def is_scheduled(self):
        return self.status.id == N_Event_Status.SCHEDULED

    def may_send_proposal(self):
        return self.status.id == N_Event_Status.SCHEDULED

    def may_create_proposal(self):
        # return self.status.id == N_Event_Status.SCHEDULED and self.proposal_set.count() == 0
        return self.proposal_set.count() == 0

    def get_requests(self):
        return self.request_set.all()

    def __str__(self):
        return self.name

    def serializable_value(self, field_name):
        if field_name not in ['customer','address','proposal','can_remove']:
            return super(Event, self).serializable_value(field_name)
        # if field_name == 'event_date':
            # return formats.date_format(self.event_date, 'Y-m-d H:m')
        if field_name == 'customer':
            return self.customer.serialize(fields=['email','first_name','last_name','suffix','prefix','cellphone','id','full_name'])
        if field_name == 'address':
            return self.address.serialize()
        if field_name == 'proposal':
            prop = self.proposal_set.first()
            if prop:
                return prop.serialize(fields=['id','status', 'invoice'])
            else:
                return None
        if field_name == 'can_remove':
            can_remove = self.can_be_removed()
            return can_remove

    def can_be_removed(self):
        return self.status.id not in [N_Event_Status.DONE]
    # def serialize(self, fields=[]):
    #
    #     if len(fields) == 0:
    #         fields = Event.default_fields
    #
    #     response = {}
    #     for fd in fields:
    #         # print(fd,self.serializable_value(fd))
    #         response[fd] = self.serializable_value(fd)
    #     return response




class Proposal(models.Model, ModelSerialize):

    DEFAULT_TOKEN_VALUE = '0'
    ERROR = -1
    ERRORS = [ERROR]
    objects = ProposalManager()
    event = models.ForeignKey(Event)
    status = models.ForeignKey('N_Proposal_Status')
    client_message = models.TextField(max_length=150, null=True, default='')
    number = models.CharField(default='0', max_length=50)
    send_token = models.CharField(default=DEFAULT_TOKEN_VALUE, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    denied_by_system = models.BooleanField(default=False)

    default_fields = ['id','status','event','items', 'can_send','can_edit', 'can_resend']

    def serializable_value(self, field_name):
        if field_name == 'event':
            return self.event.serialize()
        if field_name == 'items':
            return serialize_query(self.item_set.all())
        if field_name == 'can_send':
            cand_send = self.may_send_email() and self.status.id != N_Proposal_Status.PENDING
            return cand_send
        if field_name == 'can_resend':
            can_resend = self.may_send_email() and self.status.id == N_Proposal_Status.PENDING
            return can_resend
        if field_name == 'can_edit':
            can_edit = self.may_be_editted()
            return can_edit
        if field_name == 'invoice':
            invoice = self.invoice_set.first()
            if invoice:
                return invoice.serialize()
            return None
        return super(Proposal, self).serializable_value(field_name)

    def get_items(self):
        return self.item_set.all()

    def __str__(self):
        return self.event.name

    def get_item_by_id(self, id):
        try:
            return self.item_set.get(pk=id)
        except:
            return self.ERROR

    def add_item(self, data, business):
        try:
            oferta = data.get('oferta')
            oferta = Oferta.objects.get_oferta_by_name(name=oferta, business=business)
            discount = data.get('discount')
            unit_cost = data.get('unit_cost')
            quantity = data.get('quantity')
            tax = data.get('tax') or self.get_tax()
            description = data.get('description')

            item = Item.objects.create(tax=tax, quantity=quantity,oferta=oferta, discount=discount, description=description, unit_cost=unit_cost, proposal=self)
            # changing_item_data.send(sender=None, proposal=self)
            return item
        except Exception as e:
            print(e)
            return self.ERROR

    def add_items_list(self, data_items):
        lista = []

        for item in data_items:
            if item.get('id'):
                Item.objects.update_item(item_data=item, flush=False)
            else:
                item_entity = Item.objects.create_item(item_data=item, proposal=self, flush=False)
                lista.append(item_entity)
        Item.objects.bulk_create(lista)

    def create_items_from_requests(self, requests):
        item_list = []
        for req in requests:
            quantity = req.amount
            type = req.type
            tax = self.get_tax()
            # unit_cost = 1
            # if type.id == N_Request_Type.PRODUCT:
            print(req.get_unit_cost(), req.type)
            item = Item(quantity=quantity, type=type, tax=tax, discount=0, unit_cost=req.get_unit_cost(), proposal=self)
            if type.id == N_Request_Type.PRODUCT:
                item.product = req.product
            else:
                item.service = req.service
            # if req.has_own_tax():
            #     item.tax = req.get_tax()
            #
            # if req.has_own_discount():
            #     item.discount = req.get_discount()
            item_list.append(item)
        Item.objects.bulk_create(item_list)






    def get_total(self):
        return sum([item.grant_total() for item in self.get_items()])

    # def get_subtotal(self):
        return sum([item.sub_total() for item in self.get_items()])

    def get_subtotal(self):
        return sum([item.total() for item in self.get_items()])

    def get_taxes(self):
        return sum([item.sub_total()*item.tax for item in self.get_items()])/100

    def get_total_discount(self):
        return sum([item.total() - item.grant_total() for item in self.get_items()])

    def get_tax(self):
        return self.event.customer.business.tax / 100

    def may_send_email(self):
        return self.status.id in [N_Proposal_Status.DENIED, N_Proposal_Status.EDITTING, N_Proposal_Status.PENDING]

    def may_be_editted(self):
        return self.status.id not in [N_Proposal_Status.ACCEPTED, N_Proposal_Status.CANCELLED]


    def has_expired(self):
        return self.event.event_date.date() < datetime.date(datetime.today())

    def generate_token(self):
        if self.send_token == Proposal.DEFAULT_TOKEN_VALUE:
            token = int(datetime.today().timestamp() * 1000000)
            self.send_token = str(token)
            self.save()
            token = urlsafe_base64_encode(force_bytes(token))
        else:
            token = urlsafe_base64_encode(force_bytes(int(self.send_token)))
        return token

    def deny_by_business(self):
        if self.status.id == N_Proposal_Status.PENDING:
            self.deny(system=True)
            return self
        return self.ERROR

    def accept_by_business(self):
        if self.status.id in [N_Proposal_Status.PENDING, N_Proposal_Status.DENIED]:
            self.accept()

            return self
        return self.ERROR

    def deny(self, system=False):
        self.reset_token()
        self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.DENIED)
        self.denied_by_system = system
        self.save()

    def accept(self):
          response = Invoice.objects.create_from_proposal(proposal=self, handly=False)
          if response in Invoice.objects.ERRORS:
               return response
          self.reset_token()
          self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
          self.event.schedule()
          self.save()
          proposal_accepted.send(sender=Proposal, proposal=self)

    def reset_token(self,restart_status=False, old_status=None):
        if restart_status:
            if not old_status:
                old_status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.EDITTING)
            self.status = old_status
        self.send_token = Proposal.DEFAULT_TOKEN_VALUE
        self.save()

    def prepare_to_send(self):
        self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.PENDING)
        self.save()

    # def has_been_sent(self):
    #     self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.PENDING)
    #     self.save()



class Invoice(models.Model, ModelSerialize):

    DEFAULT_TOKEN_VALUE = '0'
    objects = InvoiceManager()
    proposal = models.ForeignKey(Proposal)
    status = models.ForeignKey('N_Invoice_Status')
    # order = models.ForeignKey(Order, null=True)
    number = models.CharField(default='0', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    send_token = models.CharField(default=DEFAULT_TOKEN_VALUE, max_length=50)
    payment_order = models.ForeignKey(PaymentOrder, null=True)
    deleted = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.now())

    def add_items_list(self, items):
        self.proposal.add_items_list(items)

    def serializable_value(self, field_name):
        # if field_name == 'proposal':
        #     return self.proposal.serialize()
        if field_name == 'can_send':
            return self.may_send_email() and self.status.id != N_Invoice_Status.PENDING
        if field_name == 'can_resend':
            return self.may_send_email() and self.status.id == N_Invoice_Status.PENDING
        if field_name == 'can_edit':
            return self.may_be_editted()
        return super(Invoice, self).serializable_value(field_name)

    default_fields = ['id','status','number','created_at','due_date','can_send','can_edit', 'can_resend']

    def update_due_date(self, due_date):
        self.due_date = due_date
        self.save()

    def __str__(self):
        return self.proposal.event.name

    def generate_token(self):
        token = int(datetime.today().timestamp() * 1000000)
        self.send_token = str(token)
        self.save()
        token = urlsafe_base64_encode(force_bytes(token))
        return token

    # def has_been_sent(self):
    #     self.status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.PENDING)
    #     self.save()
    def prepare_to_send(self):
        self.status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.PENDING)
        self.save()

    def reset_token(self, restart_status=False, old_status=None):
        self.send_token = Invoice.DEFAULT_TOKEN_VALUE
        if restart_status:
            if not old_status:
                old_status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.EDITTING)
            self.status = old_status
        self.save()

    def may_send_email(self):
        return self.status.id in [N_Invoice_Status.EDITTING, N_Invoice_Status.PENDING]

    def check_status(self):
        if self.payment_order.has_been_paid():
            self.status = N_Invoice_Status.objects.get(id=N_Invoice_Status.PAID)
            self.save()

    def set_payment(self, payment):
        self.payment_order = payment
        self.save()

    def has_payment_order(self):
        return self.payment_order != None

    def may_be_editted(self):
        return self.status.id != N_Invoice_Status.PAID

class Item(models.Model, ModelSerialize):
    objects = ItemManager()
    proposal = models.ForeignKey(Proposal)
    type = models.ForeignKey('N_Request_Type')
    product = models.ForeignKey(Product, null=True)
    service = models.ForeignKey(Service, null=True)

    tax = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(max_length=150, null=True, blank=True)

    default_fields = ['id','tax','quantity','description','discount','unit_cost', 'type', 'service', 'product']

    def serializable_value(self, field_name):

        if field_name == 'type':
            return self.type.serialize()
        if field_name == 'product':
            if self.product:
                return self.product.serialize(fields=['name','description','id'])
            else:
                return None
        if field_name == 'service':
            if self.service:
                return self.service.serialize(fields=['id','description','name'])
            else:
                return None
        if field_name == 'discount':
            return float(self.discount)
        if field_name == 'tax':
            return float(self.tax)
        if field_name == 'unit_cost':
            return float(self.unit_cost)
        return super(Item, self).serializable_value(field_name=field_name)

    def __str__(self):
        if self.type.id == N_Request_Type.PRODUCT:
            return self.product.name
        else:
            return self.service.name
        # return self.proposal.event.name

    def sub_total(self):
        return self.quantity * self.unit_cost

    def total(self):
        sub_total = self.sub_total()
        return sub_total*( 1 + self.tax/100)

    def grant_total(self):
        value = self.total()
        return value - value * self.discount / 100


class Request(models.Model):

    objects = RequestManager()

    event = models.ForeignKey(Event)
    type = models.ForeignKey('N_Request_Type')
    product = models.ForeignKey(Product, null=True)
    service = models.ForeignKey(Service, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def get_unit_cost(self):
        if self.type.id == N_Request_Type.PRODUCT:
            print(self.product.name, self.amount)
            return self.product.get_product_price(self.amount)
        else:
            return self.service.get_service_price(self.amount)
        # return 1

    # def has_own_tax(self):
    #     # if self.type.id == N_Request_Type.PRODUCT:
    #     #     return self.product.has_own_tax()
    #     # else:
    #     #     return self.service.has_own_tax()
    #     return False

    # def get_tax(self):
    #     # if self.type.id == N_Request_Type.PRODUCT:
    #     #     return self.product.get_tax()
    #     # else:
    #     #     return self.service.get_tax()
    #     return 0

    # def has_own_discount(self):
    #     # if self.type.id == N_Request_Type.PRODUCT:
    #     #     return self.product.has_own_discount()
    #     # else:
    #     #     return self.service.has_own_discount()
    #     return False
    #
    # def get_discount(self):
    #     # if self.type.id == N_Request_Type.PRODUCT:
    #     #     return self.product.get_discount()
    #     # else:
    #     #     return self.service.get_discount()
    #
    #     return 0

#Nomenclators

class N_Proposal_Status(models.Model, ModelSerialize):
    EDITTING = 1
    PENDING = 2
    ACCEPTED = 3
    DENIED = 4
    CANCELLED = 5
    default_fields = ['name','id']
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'

class N_Invoice_Status(models.Model, ModelSerialize):
    # CREATED = 1
    EDITTING = 2
    PENDING = 3
    PAID = 4
    PAST_DUE = 7
    # CANCELLED = 5
    # ACCEPTED = 6
    default_fields = ['name','id']
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'


class N_Event_Status(models.Model, ModelSerialize):

    PENDING = 1
    SCHEDULED = 2
    DONE = 3
    CANCELLED = 4
    ACCEPTED = 5
    default_fields = ['name', 'id']
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'


class N_Request_Type(models.Model, ModelSerialize):

    PRODUCT = 1
    SERVICE = 2
    default_fields = ['id','name']
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'