from django.conf import settings
from base.models import Business
from business_site.models import Website
from business_site.views import  if_user_have_website


def subscription_status(request):

    user = request.user
    if user.is_authenticated():
        groups = user.groups.all()

        PENDING = groups.count() and groups.first().name == settings.BUSINESS_TRIAL
        ACTIVE = groups.count() and groups.first().name == settings.BUSINESS_MEMBER
        EXPIRED = groups.count() and groups.first().name == settings.BUSINESS_BASIC
        return {'PENDING':PENDING,'ACTIVE':ACTIVE, 'EXPIRED':EXPIRED}
    return {}

def business_data(request):

    user = request.user
    result = {}
    if user.is_authenticated():
        b = Business.objects.filter(owner=user).first()
        result['TAX'] = b.tax
        result['BUSINESS_DATA'] = b
        if b:
            # web = Website.objects.filter(business=b).first()
            # control = WebsiteControl.objects.filter(website__business=b).first()
            WEBSITE_STATUS = None
            # if control:
            #     WEBSITE_STATUS = control.status
            #     result['WEBSITE_STATUS'] = WEBSITE_STATUS
            #     print(WEBSITE_STATUS)
            # return {'TAX':b.tax,'WEBSITE_STATUS':WEBSITE_STATUS,'BUSINESS_DATA':b}
    return result

#def i18n(request):
#    return {'available_languages': ['en', 'es', 'fr']}

# def website_status(request):
#
#     # objects = if_user_have_website(request)
#     # object = WebsiteControl.objects.filter(website=objects[0]).first()
#     user = request.user
#     if user.is_authenticated():
#
#         if not object:
#             return {'WEBSITE_STATUS':''}
#         else:
#             return {'WEBSITE_STATUS':object.status}



