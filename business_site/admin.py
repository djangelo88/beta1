from django.contrib import admin

# Register your models here.
from business_site.models import Category, Menu, Website

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Website)
