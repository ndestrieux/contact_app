from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return (Person.objects.filter(first_name__icontains=search)
                | Person.objects.filter(last_name__icontains=search)) \
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
    template_name_suffix = '_update_form'
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = ['address_forms', 'phone_forms', 'email_forms', ]
    success_message = "Contact %(first_name)s %(last_name)s updated successfully"

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.id,))

    # TODO bug when sending form when form is incorrect


class DeleteContactView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)


# Address views

class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address

    # def get_context_data(self, **kwargs):
    #     data = super(AddressDetailView, self).get_context_data(**kwargs)
    #     location = f"{self.object.street} {self.object.building_number if self.object.building_number else ''} " \
    #         f"{self.object.city} {self.object.country.name}"
    #     loc = Nominatim().geocode(location)
    #     latlng = [loc.latitude, loc.longitude]
    #     address_map = Map(location=latlng, zoom_start=18)
    #     address_map.add_child(Marker(location=latlng, popup=loc.address, icon=Icon(color='red')))
    #     data['map'] = address_map._repr_html_()
    #     return data


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Phone views

class DeletePhoneView(LoginRequiredMixin, DeleteView):
    model = Phone

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Email views

class DeleteEmailView(LoginRequiredMixin, DeleteView):
    model = Email

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


class AddContactToGroup(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = ContactGroupForm
    template_name = 'contacts_app/add_contact_to_group.html'


# Group views

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return Group.objects.filter(name__icontains=search).order_by("name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['search'] = self.request.GET.get('search')
        return data


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group


class CreateGroupView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('group-list')
    success_message = "New group added - %(name)s"


class UpdateGroupView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s updated"


class DeleteGroupView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteGroupView, self).delete(request, *args, **kwargs)
