from datetime import datetime
from django.conf import settings

from django.db import models


# Create your models here.


class StripeCustomerManager(models.Manager):

    def save_local_customer(self, customer):
        local = self.create(stripeid=customer.id, stripetoken=customer.default_source,
                            billing_email=customer.email)
        return local

class StripeCustomer(models.Model):
    objects = StripeCustomerManager()
    stripeid = models.CharField(max_length=50)
    stripetoken = models.CharField(max_length=50)
    billing_email = models.EmailField(null=True)

    def get_card(self):
        return self.card.first()

    def add_subscription(self, subscription):
        current_period_end = datetime.fromtimestamp(subscription.current_period_end)
        current_period_start = datetime.fromtimestamp(subscription.current_period_start)

        StripeSubscripcion.objects.create(stripecustomer=self, stripeid=subscription.id,
                                          stripestatus=subscription.status, current_period_start=current_period_start,
                                          current_period_end=current_period_end)
    def update_email(self, new_email):
        self.billing_email = new_email
        self.save()

    def update_source(self, new_token, new_stripe_card):
        self.stripetoken = new_token
        self.save()
        self.get_card().update_from_stripe(new_stripe_card)

    def current_subscription(self):
        return self.subscriptions.filter(current=True).first()


    class Meta:
        app_label = 'stripe_cater'

    def current_status(self):
        current_subs = self.subscriptions.filter(current=True).first()
        if not current_subs:
            return StripeSubscripcion.CANCELED
        return current_subs.stripestatus

class StripeCardManager(models.Manager):

    def save_local_card(self,stripe_card, local_customer):
        self.create(customer=local_customer,
                    stripe_id=stripe_card.id,
                    stripe_exp_month=stripe_card.exp_month,
                    stripe_exp_year=stripe_card.exp_year,
                    stripe_last4=stripe_card.last4,
                    stripe_brand=stripe_card.brand,
                    stripe_address_country=stripe_card.address_country,
                    stripe_address_city=stripe_card.address_city,
                    stripe_address_state=stripe_card.address_state,
                    stripe_address_line=stripe_card.address_line1
                    )


class StripeCard(models.Model):
    objects = StripeCardManager()
    stripe_id = models.CharField(max_length=50)
    stripe_exp_month = models.IntegerField(null=True)
    stripe_exp_year = models.IntegerField(null=True)
    stripe_last4 = models.CharField(max_length=4, null=True)
    stripe_brand = models.CharField(max_length=25, null=True)
    stripe_address_country = models.CharField(max_length=25, null=True)
    stripe_address_city = models.CharField(max_length=25, null=True)
    stripe_address_state = models.CharField(max_length=25, null=True)
    stripe_address_line = models.CharField(max_length=25, null=True)
    customer = models.ForeignKey(StripeCustomer, related_name='card')

    def get_billing_address(self):
        return "{0}, {1}, {2}, {3}".format(self.stripe_address_line,
                                           self.stripe_address_city,
                                           self.stripe_address_state,
                                           self.stripe_address_country)

    def update_from_stripe(self, stripe_card):
        self.stripe_id=stripe_card.id,
        self.stripe_exp_month=stripe_card.exp_month,
        self.stripe_exp_year=stripe_card.exp_year,
        self.stripe_last4=stripe_card.last4,
        self.stripe_brand=stripe_card.brand,
        self.stripe_address_country=stripe_card.address_country,
        self.stripe_address_city=stripe_card.address_city,
        self.stripe_address_state=stripe_card.address_state,
        self.stripe_address_line=stripe_card.address_line1
        self.save()

class StripeSubscriptionManager(models.Manager):

    def get_by_stripe_id(self, id, ignore_current_att = False):
        query = self.filter(stripeid=id)
        if not ignore_current_att:
            query.filter(current=True)

        return query.first()

class StripeSubscripcion(models.Model):
    TRIAL = 'trialing'
    ACTIVE = 'active'
    PAST_DUE = 'past_due'
    CANCELED = 'canceled'
    UNPAID = 'unpaid'

    STATUS_CHOICES=(
        ('trialing', TRIAL),
        ('active', ACTIVE),
        ('past_due', PAST_DUE),
        ('canceled', CANCELED),
        ('unpaid', UNPAID),
        )

    objects = StripeSubscriptionManager()
    stripeid = models.CharField(max_length=50)
    stripestatus = models.CharField(max_length=50)
    stripecustomer = models.ForeignKey(StripeCustomer, related_name='subscriptions')
    current = models.BooleanField(default=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()

    def update_from_stripe(self, subscription_json):


        self.stripestatus = subscription_json['status']
        self.save()

    def cancel(self):
        self.current = False
        self.save()

    class Meta:
        app_label = 'stripe_cater'

    def add_invoice(self, invoice):
        created_at = datetime.fromtimestamp(invoice['date'])
        StripeInvoice.objects.create(subscription=self, stripeid=invoice['id'],
                                     created_at=created_at, receipt_number=invoice['receipt_number'])

    def update_billing_cycle(self, start, end):
        self.current_period_start =  start
        self.current_period_end = end
        self.save()

    def find_invoice(self, stripe_id):
        return self.stripeinvoice_set.filter(stripe_id=stripe_id).first()

    def get_billing_receipts(self):
        return self.invoices.filter(paid=True)

class StripeInvoice(models.Model):

    stripeid = models.CharField(max_length=50)
    subscription = models.ForeignKey(StripeSubscripcion, related_name="invoices")
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    attempt_count = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(null=True)
    closed = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=50, null=True)

    def failed(self, invoice_json):
        self.attempt_count = (invoice_json['attempt_count'])
        self.last_attempt = datetime.fromtimestamp((invoice_json['date']))
        self.closed = invoice_json['closed']
        self.save()


    def success(self, invoice_json):
        self.paid = True
        self.closed = True
        self.receipt_number = invoice_json['receipt_number']
        self.save()

class EventRecord(models.Model):

    stripeid = models.CharField(max_length=50)

class PaymentOrderManager(models.Manager):

    def create_paymanet(self, amount):
        return self.create(amount=amount)

class PaymentOrder(models.Model):

    AMOUNT_ERROR=-1

    objects = PaymentOrderManager()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    current = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def due(self):
        return self.amount - self.current

    def init_charge(self, amount,destination):
        if amount > self.due():
            return self.AMOUNT_ERROR

        charge = Charge(payment=self,
                        amount=amount,
                        destination=destination
                        )
        return charge

    def save_charge(self, charge):
        if charge.status != Charge.PAID:
            raise RuntimeError()
        charge.save()
        self.current = self.current + charge.amount
        self.save()

    def has_been_paid(self):
        return self.current >= self.amount

    def update_amount(self, new_amount):
        self.amount = new_amount
        self.save()


class ChargeManager(models.Manager):

    def get_charge(self, id):
        return self.filter(id=id).first()

class Charge(models.Model):
    PAID = 'PAID'
    PENDING = 'PENDING'
    FAILED = 'FAILED'

    STATUS_CHOICE = (('PAID',PAID),('FAILED',FAILED),('PENDING',PENDING))

    objects = ChargeManager()
    payment = models.ForeignKey(PaymentOrder)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    captured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    captured_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, default=PENDING)
    destination = models.CharField(max_length=50)
    stripe_id = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, default=settings.STRIPE_DEFAULT_CURRENCY)

    def get_amount_ready_to_charge_by_stripe(self):
        return self.amount * 100 # amount in cents


class StripeAccountManager(models.Manager):

    def create_account(self, stripe_publishable_key, access_token, stripe_user_id):
       return self.create(stripe_publishable_key=stripe_publishable_key, access_token=access_token, stripe_user_id=stripe_user_id)

class StripeAccount(models.Model):

    objects = StripeAccountManager()
    stripe_publishable_key = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    stripe_user_id = models.CharField(max_length=50)
