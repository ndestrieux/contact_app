from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView

from contacts_app.forms import PersonForm, ContactGroupForm, UserRegistrationForm, PhoneFormSet, \
    EmailFormSet, AddressFormSet
from contacts_app.models import Person, Address, Phone, Email, Group


# Create your views here.

# User registration view

class UserRegistration(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = "User %(username)s has been registered"
    success_url = reverse_lazy('login')


# Formset Success Message Mixin

class FormSetSuccessMessageMixin(object):
    success_message = ''

    def forms_valid(self, form, inlines):
        response = super(FormSetSuccessMessageMixin, self).forms_valid(form, inlines)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


# Person views

class ContactListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10

    def get_queryset(self):
        current_user_person_query = Person.objects.filter(created_by=self.request.user)
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return (current_user_person_query.filter(first_name__icontains=search)
                | current_user_person_query.filter(last_name__icontains=search)) \
            .order_by("last_name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['search'] = self.request.GET.get('search')
        return data


class CreateContactView(LoginRequiredMixin, FormSetSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Person
    form_class = PersonForm
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = ['address_forms', 'phone_forms', 'email_forms', ]
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s created"


class UpdateContactView(LoginRequiredMixin, FormSetSuccessMessageMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Person
    form_class = PersonForm
    group_form_class = ContactGroupForm
    template_name_suffix = '_update_form'
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = ['address_forms', 'phone_forms', 'email_forms', ]
    success_message = "Contact %(first_name)s %(last_name)s updated successfully"

    def get_queryset(self):
        get_object_or_404(Person, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.id,))


class DeleteContactView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def get_queryset(self):
        get_object_or_404(Person, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)


# Address views

class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address

    def get_queryset(self):
        get_object_or_404(Address, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address

    def get_queryset(self):
        get_object_or_404(Address, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Phone views

class DeletePhoneView(LoginRequiredMixin, DeleteView):
    model = Phone

    def get_queryset(self):
        get_object_or_404(Phone, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Email views

class DeleteEmailView(LoginRequiredMixin, DeleteView):
    model = Email

    def get_queryset(self):
        get_object_or_404(Email, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


class AddContactToGroup(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = ContactGroupForm
    template_name = 'contacts_app/add_contact_to_group.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['groups'].queryset = Group.objects.filter(created_by=self.request.user.pk)
        return form

    def get_queryset(self):
        get_object_or_404(Person, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.id,))


# Group views

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 10

    def get_queryset(self):
        current_user_group_query = Group.objects.filter(created_by=self.request.user)
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return current_user_group_query.filter(name__icontains=search).order_by("name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['search'] = self.request.GET.get('search')
        return data


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group

    def get_queryset(self):
        get_object_or_404(Group, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()


class CreateGroupView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Group
    fields = ['name', 'description', ]
    success_url = reverse_lazy('group-list')
    success_message = "New group added - %(name)s"


class UpdateGroupView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    fields = ['name', 'description', ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s updated"

    def get_queryset(self):
        get_object_or_404(Group, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()


class DeleteGroupView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s deleted"

    def get_queryset(self):
        get_object_or_404(Group, id=self.kwargs.get('pk'), created_by=self.request.user)
        return super().get_queryset()

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteGroupView, self).delete(request, *args, **kwargs)
