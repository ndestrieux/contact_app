from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django import forms
from extra_views import InlineFormSetFactory
from django_select2 import forms as s2forms


from contacts_app.models import Person, Phone, Email, Address, Group, User


class CurrentUserFormMixin:
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_by = self.current_user
        if commit:
            instance.save()
        return instance


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class GroupWidget(s2forms.ModelSelect2MultipleWidget):
    # select2 widget to add group to person
    model = Group
    search_fields = ["name__icontains"]


class PersonForm(CurrentUserFormMixin, forms.ModelForm):
    first_name = forms.CharField(validators=[RegexValidator("^((\w)+([-'])*(\w)+)$")])
    last_name = forms.CharField(validators=[RegexValidator("^((\w)+([-'])*(\w)+)$")])

    class Meta:
        model = Person
        exclude = [
            "created_by",
        ]
        widgets = {"groups": GroupWidget(attrs={"data-width": "100%"})}


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = [
            "person",
        ]
        widgets = {"type": forms.HiddenInput()}


class PhoneForm(forms.ModelForm):
    def clean_type(self):
        phone_type = self.cleaned_data.get("type")
        if phone_type is None:
            return self.fields["type"].initial
        return phone_type

    class Meta:
        model = Phone
        exclude = [
            "person",
        ]


class EmailForm(forms.ModelForm):
    def clean_type(self):
        email_type = self.cleaned_data.get("type")
        if email_type is None:
            return self.fields["type"].initial
        return email_type

    class Meta:
        model = Email
        exclude = [
            "person",
        ]


class AddressFormSet(InlineFormSetFactory):
    model = Address
    form_class = AddressForm
    factory_kwargs = {"extra": 2, "max_num": 2, "can_delete": False}
    initial = [{"type": 1}, {"type": 2}]

    def get_initial(self):
        initial = self.initial[:]
        if "pk" in self.kwargs:
            if Address.objects.filter(person_id=self.kwargs["pk"], type=1).exists():
                initial.remove({"type": 1})
            if Address.objects.filter(person_id=self.kwargs["pk"], type=2).exists():
                initial.remove({"type": 2})
        return initial


class PhoneFormSet(InlineFormSetFactory):
    model = Phone
    form_class = PhoneForm
    factory_kwargs = {"extra": 1, "can_delete": False}


class EmailFormSet(InlineFormSetFactory):
    model = Email
    form_class = EmailForm
    factory_kwargs = {"extra": 1, "can_delete": False}


class MemberWidget(s2forms.ModelSelect2MultipleWidget):
    # select2 widget to add person to group
    model = Person
    search_fields = ["first_name__icontains", "last_name__icontains"]


class UpdateGroupForm(CurrentUserFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["members"].queryset = Person.objects.filter(
            created_by=self.current_user
        )
        self.fields["members"].required = False

    class Meta:
        model = Group
        fields = [
            "name",
            "members",
            "description",
        ]

    members = forms.ModelMultipleChoiceField(queryset=None, widget=MemberWidget)
