from datetime import datetime
from django.forms.forms import Form
from django import forms
from base.models import N_Country, N_State


class BookingForm(Form):

    cliente_name = forms.CharField(max_length=50)
    cliente_last_name = forms.CharField(max_length=50)
    cliente_email = forms.EmailField()
    cliente_phone = forms.CharField(max_length=50)
    # cliente_address = forms.CharField(max_length=125)
    cliente_birthday = forms.DateField(required=False)
    cliente_first_line = forms.CharField(max_length=150)
    cliente_second_line = forms.CharField(max_length=150, required=False)
    cliente_zip = forms.IntegerField(min_value=40)
    cliente_city = forms.CharField()
    cliente_country = forms.ModelChoiceField(queryset=N_Country.objects.all())
    cliente_state = forms.ModelChoiceField(queryset=N_State.objects.all())

    evento_name = forms.CharField(max_length=100)
    evento_date = forms.DateTimeField()
    # evento_address = forms.CharField(max_length=125)
    evento_first_line = forms.CharField(max_length=150)
    evento_second_line = forms.CharField(max_length=150, required=False)
    evento_zip = forms.IntegerField(min_value=40)
    evento_city = forms.CharField()
    evento_country = forms.ModelChoiceField(queryset=N_Country.objects.all())
    evento_state = forms.ModelChoiceField(queryset=N_State.objects.all())


    def clean_evento_date(self):
        print(self.data['evento_date'])
        #print(self.fields['event_date'].to_python((self.data['event_date'])))
        #print(datetime.today().timestamp())
        if self.fields['evento_date'].to_python((self.data['evento_date'])).date() < datetime.today().date():
            raise forms.ValidationError('La fecha del evento debe ser posterior al fecha actual')
        return  self.data['evento_date']