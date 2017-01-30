from django.conf import settings
from django.db import models
from base.models import Business
# Create your models here.


class Website(models.Model):
    template = models.IntegerField(default=1)#Ahora este campo es estatico
    business = models.ForeignKey(Business, default=0, related_name='website')

    def __str__(self):
        return self.business.name



class WebDomain(models.Model):
    domain = models.CharField(max_length=50, blank=False)
    website = models.OneToOneField(Website, default=0)

    def __str__(self):
        return self.domain


class BasicInfo(models.Model):
    logo = models.FileField(upload_to='photos', null=True)
    description = models.CharField(max_length=250, blank=False)
    website = models.OneToOneField(Website, default=0)


class Gallery(models.Model):
    comments = models.CharField(max_length=50, blank=True)
    # background = models.FileField(upload_to=settings.MEDIA_ROOT+'/photos', blank=False)
    website = models.OneToOneField(Website)


class Photo(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.FileField(upload_to='photos', blank=False)
    asbackground = models.BooleanField(default=False)
    gallery = models.ForeignKey(Gallery)

class Category(models.Model):
    description = models.CharField(max_length=100)
    website = models.ForeignKey(Website)

    class Meta:
        unique_together = (('description','website'),)

    def __str__(self):
        return self.description

class Menu(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=150, null=True, blank=True)
    # price = models.FloatField(default=0.00, null=False)
    image = models.FileField(upload_to='photos')
    comments = models.TextField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category)

class MenuPrice(models.Model):
    min = models.IntegerField(null=False)
    max = models.IntegerField(null=False)
    price = models.FloatField(null=False, default=0.00)
    menu = models.ForeignKey(Menu)
    def get_total(self):
        return self.max*self.price

class StaffServices(models.Model):
    service = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=250, null=True, blank=True)
    image = models.FileField(upload_to='photos')
    price = models.FloatField(default=0.00, null=False)
    website = models.ForeignKey(Website)


class Links(models.Model):
    twitter = models.URLField(default="twitter.com", null=True)
    instagram = models.URLField(default="instagram.com", null=True)
    facebookpage = models.URLField(default="facebook.com", null=True)
    yelp = models.URLField(default="yelp.com", null=True)
    gplus = models.URLField(default="gplus.com", null=True)
    website = models.OneToOneField(Website)


class ContactUs(models.Model):
    phone = models.CharField(max_length=15,null=False)
    email = models.EmailField()
    address = models.CharField(max_length=100, null=True)
    website = models.OneToOneField(Website)


class WebsiteControl(models.Model):
    status = models.IntegerField(default=0)#(0-create, 1-template, 2-basic, 3-gallery,4-Menu, 5-Staff, 6-links, 7-contact, 8-publish)
    website = models.OneToOneField(Website)