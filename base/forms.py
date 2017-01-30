from datetime import datetime
from re import match

from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.forms.models import ModelForm, ModelChoiceField
from django.forms.widgets import Textarea, PasswordInput

from base.model_invoice import Event
from base.models import Customer, Business, N_State, N_Country


# widgets
class SubscriptionModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.description

# forms

class CustomerForm(ModelForm):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    comments = forms.CharField(max_length=250, widget=Textarea, required=False)
    company = forms.CharField(max_length=50, required=False)
    birthday = forms.DateField(required=False, label='Fecha de nacimiento')
    cellphone = forms.CharField(required=False, max_length=25, label='Telefono movil')
    phone_home = forms.CharField(required=False, max_length=25, label='Telefono casa')
    address = forms.CharField(required=False, max_length=250, widget=Textarea,label='Dirección')

    class Meta:
        model = Customer
        fields = ['suffix','prefix']

    def clean_cellphone(self):
        value = self.data['cellphone']
        if value:
            flag =  match(r'^[+]{0,1}\d+$',value)
            if flag:
                return value
            else:
                raise forms.ValidationError('Numero de telefono invalido')
        return value

    def clean_phone_home(self):
        value = self.data['phone_home']
        if value:
            flag =  match(r'^[+]{0,1}\d+$',value)
            if flag:
                return value
            else:
                raise forms.ValidationError('Numero de telefono invalido')
        return value

class BusinessForm(Form):

    phone = forms.CharField(max_length=20, error_messages={'required':'Campo Requerido'},widget=forms.TextInput(attrs={'placeholder':"Phone"}))
    name = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder':"Business name"}))
    first_name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'placeholder':"First name"}))
    last_name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'placeholder':"Last name"}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':"Password"}), max_length=25)
    password_confirm = forms.CharField(widget=PasswordInput(attrs={'placeholder':"Password confirm"}), max_length=25)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':"Email"}))
    # address = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder':"Address"}))
    #subscriptions = SubscriptionModelChoiceField(queryset=SubscriptionType.objects.all(), widget=RadioSelect, empty_label=None, to_field_name="id")
    tax = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0,widget=forms.NumberInput(attrs={'placeholder':"Tax"}))
    first_line = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder':"First Line"}))
    second_line = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder':"Second Line"}))
    zip = forms.IntegerField(min_value=40,widget=forms.TextInput(attrs={'placeholder':"Codigo Postal"}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Ciudad"}))
    state = forms.ModelChoiceField(queryset=N_State.objects.all())
    country = forms.ModelChoiceField(queryset=N_Country.objects.all(),empty_label='--Seleccione un pais--')



    def clean_password_confirm(self):
            if self.data['password'] != '' and self.data['password'] != self.data['password_confirm']:
                raise forms.ValidationError('La contraseña y su confirmación no coinciden.')
            return self.data['password_confirm']

class BusinessProfileForm(Form):

    phone = forms.CharField(max_length=20, error_messages={'required':'Campo Requerido'})
    name = forms.CharField(max_length=250)
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()
    address = forms.CharField(max_length=250, widget=forms.Textarea())
    tax = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0)
    logo = forms.FileField(required=False)
    websiteurl = forms.URLField(required=False)
    default_site = forms.BooleanField(required=False)

# class CaterAuthenticationForm(AuthenticationForm):
#
#     def confirm_login_allowed(self, user):
#
#         AuthenticationForm.confirm_login_allowed(self, user)
#
#         subs_disable_message = "Su suscripcion vigente no esta activada o ha expirado."
#
#         groups = user.groups.all()
#         if(len(groups)) and groups.first().name in settings.BUSINESS_GROUPS:
#             b = Business.objects.filter(owner=user).first()
#             sub = b.subscription_set.filter(current=True).first()
#             if sub.expire_date < datetime.date(datetime.today()) or not sub.is_active():
#
#                 raise forms.ValidationError(
#                 subs_disable_message,
#                 code='invalid_subscription',
#                 # params={'username': self.username_field.verbose_name},
#             )

    # def clean(self):
    #
    #     subs_disable_message = "Su suscripcion vigente no esta activada o ha expirado."
    #
    #     cleaned_data = AuthenticationForm.clean(self)
    #
    #     if cleaned_data.get('username'):
    #         user = User.objects.filter(email=cleaned_data.get('username')).first()
    #
    #         groups = user.groups.all()
    #         if(len(groups)) and groups.first().name in settings.BUSINESS_GROUPS:
    #             b = Business.objects.filter(owner=user).first()
    #             sub = b.subscription_set.filter(current=True).first()
    #             if sub.expire_date > datetime.date(datetime.today()) and sub.active:
    #                 return cleaned_data
    #             else:
    #                 raise forms.ValidationError(
    #                 subs_disable_message,
    #                 code='invalid_subscription',
    #                 # params={'username': self.username_field.verbose_name},
    #             )
    #         else:
    #             return cleaned_data
    #
    #     return cleaned_data

# class CustomerModelChoice(ModelChoiceField):
#
#     def __init__(self,queryset, initial=None,*args, **kwargs):
#         print('hola')
#         print(initial)
#         super(CustomerModelChoice, self).__init__(queryset,initial=initial, *args, **kwargs)




class PasswordReset(PasswordResetForm):

    def clean_email(self):
        user = User.objects.filter(email=self.data['email']).filter(is_active=True).first()
        if not user:
            raise forms.ValidationError('Email Invalido')
        return self.data['email']

class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    event_date = forms.DateTimeField()
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())



    def __init__(self,*args, **kwargs):
        print(kwargs)
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.list_by_business(business=kwargs.get('initial').get('business'))

    class Meta:
        model = Event
        exclude = ['status']

class ProposalEventForm(EventForm):
    # due_date = forms.DateField()
    comment = forms.CharField(widget=forms.Textarea(), max_length=150, required=False)

    def clean_event_date(self):
        print(self.data['event_date'])
        #print(self.fields['event_date'].to_python((self.data['event_date'])))
        #print(datetime.today().timestamp())
        if self.fields['event_date'].to_python((self.data['event_date'])).date() < datetime.today().date():
            raise forms.ValidationError('La fecha del evento debe ser posterior al fecha actual')
        return  self.data['event_date']

    # def clean_due_date(self):
    #     due_date = self.fields['due_date'].to_python((self.data['due_date']))
    #     event_date = self.fields['event_date'].to_python((self.data['event_date'])).date()
    #     if due_date > event_date:
    #         raise forms.ValidationError('La fecha de pago debe ser anterior a la fecha del evento')
    #     if due_date < datetime.today().date():
    #         raise forms.ValidationError('La fecha de pago debe ser posterior a la fecha actual')
    #     return self.data['due_date']

class InvoiceEventForm(EventForm):
    due_date = forms.DateField()
    comment = forms.CharField(widget=forms.Textarea(), max_length=150, required=False)

    def clean_event_date(self):
        #print(self.data['event_date'])
        #print(self.fields['event_date'].to_python((self.data['event_date'])))
        #print(datetime.today().timestamp())
        if self.fields['event_date'].to_python((self.data['event_date'])).date() < datetime.today().date():
            raise forms.ValidationError('La fecha del evento debe ser posterior al fecha actual')
        return  self.data['event_date']

    # def clean_due_date(self):
    #     due_date = self.fields['due_date'].to_python((self.data['due_date']))
    #     event_date = self.fields['event_date'].to_python((self.data['event_date'])).date()
    #     if due_date > event_date:
    #         raise forms.ValidationError('La fecha de pago debe ser anterior a la fecha del evento')
    #     if due_date < datetime.today().date():
    #         raise forms.ValidationError('La fecha de pago debe ser posterior a la fecha actual')
    #     return self.data['due_date']


class ItemForm(forms.Form):

    description = forms.CharField(max_length=150, widget=forms.Textarea(), required=False)
    quantity = forms.IntegerField(min_value=0)
    discount = forms.DecimalField(max_digits=4, decimal_places=2, initial=0, min_value=0)
    unit_cost = forms.DecimalField(max_digits=9, decimal_places=2, min_value=0)
    oferta = forms.CharField(max_length=50)
    tax = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0)

class BillingEmailForm(forms.Form):

    email = forms.EmailField()



class CustomerImportForm(forms.Form):

    excel = forms.FileField(required=True)

    # def clean_excel(self):
    #     print(self.data)
    #     return self.data['excel']

class TestForm(Form):

    asignatura = forms.CharField(max_length=25)
    nota = forms.IntegerField(max_value=20)