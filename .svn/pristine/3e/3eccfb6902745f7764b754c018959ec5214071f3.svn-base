from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from base.model_invoice import Invoice, Proposal
from base.models import Business, Customer
from stripe_cater.models import StripeSubscripcion


class Command(BaseCommand):

    def handle(self, *args, **options):
        memeber_group = Group.objects.get_by_natural_key(name=settings.BUSINESS_MEMBER)
        trial_group = Group.objects.get_by_natural_key(name=settings.BUSINESS_TRIAL)
        basic_group = Group.objects.get_by_natural_key(name=settings.BUSINESS_BASIC)
        # *
        permissions = []
        content_type = ContentType.objects.get_for_model(Business)
        p = Permission.objects.update_or_create(name='Can update profile', codename='update_profile', content_type=content_type)
        permissions.append(p)
        content_type = ContentType.objects.get_for_model(Customer)
        p = Permission.objects.update_or_create(name='Can add customer', codename='add_customer', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can edit customer', codename='edit_customer', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can remove customer', codename='remove_customer', content_type=content_type)
        permissions.append(p)
        content_type = ContentType.objects.get_for_model(Proposal)

        p = Permission.objects.update_or_create(name='Can list proposal', codename='list_proposal', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can view proposal', codename='view_proposal', content_type=content_type)
        permissions.append(p)
        content_type = ContentType.objects.get_for_model(Invoice)

        p = Permission.objects.update_or_create(name='Can list invoice', codename='list_invoice', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can view invoice', codename='view_invoice', content_type=content_type)
        permissions.append(p)
        for p in permissions:
            print(p[0])
            memeber_group.permissions.add(p[0])
            trial_group.permissions.add(p[0])
            basic_group.permissions.add(p[0])
        # [TRIAL,MEMBER]
        permissions = []
        content_type = ContentType.objects.get_for_model(Proposal)
        p = Permission.objects.update_or_create(name='Can create or update proposal', codename='create_update_proposal', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can mail proposal', codename='mail_proposal', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can deny proposal', codename='deny_proposal', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can accept proposal', codename='accept_proposal', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can delete proposal', codename='delete_proposal', content_type=content_type)
        permissions.append(p)
        content_type = ContentType.objects.get_for_model(Invoice)

        p = Permission.objects.update_or_create(name='Can create or update invoice', codename='create_update_invoice', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can mail invoice', codename='mail_invoice', content_type=content_type)
        permissions.append(p)
        p = Permission.objects.update_or_create(name='Can delete invoice', codename='delete_invoice', content_type=content_type)
        permissions.append(p)
        for p in permissions:
            trial_group.permissions.add(p[0])
            memeber_group.permissions.add(p[0])
        # BASIC
        content_type = ContentType.objects.get_for_model(StripeSubscripcion)
        p = Permission.objects.update_or_create(name='Can update subcription', codename='update_subscription', content_type=content_type)
        permissions.append(p)
        for p in permissions:
            basic_group.permissions.add(p[0])