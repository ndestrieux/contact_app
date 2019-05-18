from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django import forms
from extra_views import InlineFormSet

from contacts_app.models import Person, Phone, Email, Address, PHONE_TYPE, EMAIL_TYPE


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class PersonForm(forms.ModelForm):
    first_name = forms.CharField(validators=[RegexValidator('^((\w)+([-\'])*(\w)+)$')])
    last_name = forms.CharField(validators=[RegexValidator('^((\w)+([-\'])*(\w)+)$')])

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'description']


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['person', ]
        widgets = {
            'type': forms.HiddenInput()
        }


class PhoneForm(forms.ModelForm):
    # number = forms.CharField(
    #     widget=forms.TextInput(attrs={'type': 'number'}),
    #     validators=[MinValueValidator(1), MaxValueValidator(9999999999999999)],
    #     error_messages={'invalid': 'Enter a valid phone number'},
    # )
    number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=PHONE_TYPE[1:],
        required=False
    )

    def clean_type(self):
        phone_type = self.cleaned_data.get('type')
        if phone_type is None:
            return self.fields['type'].initial
        else:
            return phone_type

    class Meta:
        model = Phone
        exclude = ['person', ]
        widgets = {
            'phone': forms.TextInput()
        }


class EmailForm(forms.ModelForm):
    address = forms.EmailField(error_messages={'invalid': 'Enter a valid email address'},)
    type = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=EMAIL_TYPE[1:],
        required=False
    )

    def clean_type(self):
        email_type = self.cleaned_data.get('type')
        if email_type is None:
            return self.fields['type'].initial
        else:
            return email_type

    class Meta:
        model = Email
        exclude = ['person', ]


class ContactGroupForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['groups']
        labels = {
            'groups': ''
        }


class AddressFormSet(InlineFormSet):
    model = Address
    form_class = AddressForm
    factory_kwargs = {'extra': 2, 'max_num': 2, 'can_delete': False}
    initial = [{'type': 1}, {'type': 2}]


class PhoneFormSet(InlineFormSet):
    model = Phone
    form_class = PhoneForm
    factory_kwargs = {'extra': 1, 'can_delete': False}


class EmailFormSet(InlineFormSet):
    model = Email
    form_class = EmailForm
    factory_kwargs = {'extra': 1, 'can_delete': False}
