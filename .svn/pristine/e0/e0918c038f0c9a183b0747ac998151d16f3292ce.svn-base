from django.forms.models import ModelForm

__author__ = 'maykel'

from django import forms
from business_site.models import Menu, StaffServices, Category
from base.models import Business


class TemplateChoice(forms.Form):
    template = forms.ChoiceField(required=True, initial=1, choices=((1, 'Template 1'), ), widget=forms.RadioSelect())


class BasicInfoForm(forms.Form):
    # form1 wizard
    # company_name = forms.CharField(widget=forms.TextInput, max_length=100)
    logo = forms.FileField(widget=forms.FileInput, required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Descripción de su negocio"}), max_length=250, required=True)


class GalleryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=200, required=False)
    image = forms.FileField(widget=forms.FileInput, required=True)
class PhotoEditForm(GalleryForm):
    image = forms.FileField(widget=forms.FileInput, required=False)

class CategoryForm(forms.Form):
    description = forms.CharField(widget=forms.TextInput, max_length=150, required=True)

class MenuForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=150, required=True)
    description = forms.CharField(widget=forms.Textarea, max_length=250, required=False)
    image = forms.FileField(widget=forms.FileInput, required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    min = forms.IntegerField(widget=forms.NumberInput, min_value=1, required=True)
    max = forms.IntegerField(widget=forms.NumberInput, min_value=2, required=True)
    price = forms.DecimalField(widget=forms.NumberInput, decimal_places=2, min_value=0, required=True)


    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(website=kwargs.get('initial').get('website'))


class MenuEdit(MenuForm):
    image = forms.FileField(widget=forms.FileInput, required=False)

class StaffForm(ModelForm):
    price = forms.DecimalField(min_value=0, required=False)
    class Meta:
        model = StaffServices
        fields = ['service', 'description', 'image']



class StaffEditForm(StaffForm):
    service = forms.CharField(widget=forms.TextInput, max_length=250, required=False)
    image = forms.FileField(widget=forms.FileInput, required=False)

class SendMessageForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput, max_length=250, required=True)
    email = forms.EmailField(widget=forms.EmailInput, max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=450, required=True)

class LinksForm(forms.Form):
    twitter = forms.URLField(widget=forms.TextInput, max_length=255, required=False)
    instagram = forms.URLField(widget=forms.TextInput, max_length=255, required=False)
    facebook_page = forms.URLField(widget=forms.TextInput, max_length=255, required=False)
    yelp = forms.URLField(widget=forms.TextInput, max_length=255, required=False)
    gplus = forms.URLField(widget=forms.TextInput, max_length=255, required=False)


class ContactUsForm(forms.Form):
    # fields = {'country_code': forms.CharField(), 'phone_number': forms.IntegerField(),
    #           'extension': forms.IntegerField()}
    # phone = forms.PhoneField(fields=fields, widget=forms.MultiValueField, required=False)
    phone = forms.CharField(widget=forms.TextInput, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    address = forms.CharField(widget=forms.Textarea, max_length=255, required=False)
