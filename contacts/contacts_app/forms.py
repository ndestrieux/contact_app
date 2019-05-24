from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django import forms
from extra_views import InlineFormSetFactory

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
        exclude = ['groups', 'created_by', ]


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['person', 'created_by', ]
        widgets = {
            'type': forms.HiddenInput()
        }


class PhoneForm(forms.ModelForm):
    number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=PHONE_TYPE[0:],
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
        exclude = ['person', 'created_by', ]
        widgets = {
            'phone': forms.TextInput()
        }


class EmailForm(forms.ModelForm):
    address = forms.EmailField(error_messages={'invalid': 'Enter a valid email address'},)
    type = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=EMAIL_TYPE[0:],
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
        exclude = ['person', 'created_by', ]


class ContactGroupForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['groups']
        labels = {
            'groups': ''
        }


class AddressFormSet(InlineFormSetFactory):
    model = Address
    form_class = AddressForm
    factory_kwargs = {'extra': 2, 'max_num': 2, 'can_delete': False}
    initial = [{'type': 1}, {'type': 2}]

    def get_initial(self):
        initial = self.initial[:]
        if 'pk' in self.kwargs:
            if Address.objects.filter(person_id=self.kwargs['pk'], type=1).exists():
                initial.remove({'type': 1})
            if Address.objects.filter(person_id=self.kwargs['pk'], type=2).exists():
                initial.remove({'type': 2})
        return initial


class PhoneFormSet(InlineFormSetFactory):
    model = Phone
    form_class = PhoneForm
    factory_kwargs = {'extra': 1, 'can_delete': False}


class EmailFormSet(InlineFormSetFactory):
    model = Email
    form_class = EmailForm
    factory_kwargs = {'extra': 1, 'can_delete': False}
