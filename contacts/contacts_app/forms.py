from django import forms
from django.forms.models import inlineformset_factory
from .models import Person, Phone, Email, Address


#
#
# PhoneFormSet = inlineformset_factory(Person, Phone, fields='__all__', extra=1)
# EmailFormSet = inlineformset_factory(Person, Email, fields='__all__', extra=1)


# class AddressForm(forms.ModelForm):
#
#     class Meta:
#         model = Address
#         fields = '__all__'
#
#     # def __init__(self):
