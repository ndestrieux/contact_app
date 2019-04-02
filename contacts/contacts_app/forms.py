from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django import forms

from contacts_app.models import Person, Phone, Email


class PersonForm(forms.ModelForm):
    first_name = forms.CharField(validators=[RegexValidator('^((\w)+([-\'])*(\w)+)$')])
    last_name = forms.CharField(validators=[RegexValidator('^((\w)+([-\'])*(\w)+)$')])

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'description']


class PhoneForm(forms.ModelForm):
    number = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999999999999999)],
        error_messages={'invalid': 'Enter a valid phone number'},
    )

    class Meta:
        model = Phone
        fields = '__all__'


class EmailForm(forms.ModelForm):
    address = forms.EmailField(error_messages={'invalid': 'Enter a valid email address'},)

    class Meta:
        model = Email
        fields = '__all__'


class ContactGroupForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['groups']
        labels = {
            'groups': ''
        }