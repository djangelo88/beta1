__author__ = 'maykel'
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from business_site.views import WebsiteTemplate, WebsiteBasics, WebsiteGallery, WebsiteLinks, WebsiteContactUs, WebsiteCheck, WebsitePreview,\
    WebsiteCongrats, Photos, PhotosRemove, PhotosAdd, PhotosEdit, Menucategory, MenucategoryAdd, MenuAdd, MenuList, MenuEdit, Unpublish, MenuRemove, StaffList, \
    StaffAdd, StaffRemove, StaffEdit, Publish, CategorySelectView

urlpatterns = patterns('',
    # Examples:
   # url(r'^$', BusinessSiteWizard.as_view([HeadInfo, BusinessInfo, ContactInfo]), name='wizard'),

    url(r'^websiteinit', WebsiteCheck.as_view(), name='websiteinit'),
    url(r'^template', login_required(WebsiteTemplate.as_view()), name='template'),
    url(r'^basic_info', login_required(WebsiteBasics.as_view()), name='basic_info'),
    url(r'^photos/$', login_required(Photos.as_view()), name='photos'),
    url(r'^photos/add$', login_required(PhotosAdd.as_view()), name='photos_add'),
    url(r'^photos/edit/(?P<id>\d+)$', login_required(PhotosEdit.as_view()), name='photos_edit'),
    url(r'^photos/remove/(?P<id>\d+)$', login_required(PhotosRemove.as_view()), name='photos_remove'),

    url(r'^gallery', login_required(WebsiteGallery.as_view()), name='gallery'),
    url(r'^category$', Menucategory.as_view(), name='category'),
    url(r'^category/add$', MenucategoryAdd.as_view(), name='add_category'),
    url(r'^category/list/(?P<id>\d+)', CategorySelectView.as_view(), name="category_list"),
    url(r'^menu$', MenuList.as_view(), name='menu'),
    url(r'^menu/add$', MenuAdd.as_view(), name='add_menu'),
    url(r'^menu/edit/(?P<id>\d+)$', MenuEdit.as_view(), name='edit_menu'),
    url(r'^menu/remove/(?P<id>\d+)$', MenuRemove.as_view(), name='remove_menu'),
    url(r'^staffandservice$', login_required(StaffList.as_view()), name='staffandservice'),
    url(r'^staffandservice/add$', login_required(StaffAdd.as_view()), name='add_staffandservice'),
    url(r'^staffandservice/remove/(?P<id>\d+)$', StaffRemove.as_view(), name='remove_staff'),
    url(r'^staffandservice/edit/(?P<id>\d+)$', StaffEdit.as_view(), name='edit_staff'),
    url(r'^links', login_required(WebsiteLinks.as_view()), name='links'),
    url(r'^contactus',login_required(WebsiteContactUs.as_view()), name='contactus'),
    url(r'^preview', login_required(WebsitePreview.as_view()), name='preview'),
    url(r'^congrats', login_required(WebsiteCongrats.as_view()), name='congrats'),
    url(r'^unpublish', Unpublish.as_view(), name='unpublish'),
    url(r'^publish', Publish.as_view(), name='publish'),
)