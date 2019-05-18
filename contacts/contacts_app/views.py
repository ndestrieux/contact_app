from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView

from contacts_app.forms import PersonForm, PhoneForm, EmailForm, ContactGroupForm, UserRegistrationForm, PhoneFormSet, \
    EmailFormSet, AddressFormSet, AddressForm
from contacts_app.models import Person, Address, Phone, Email, Group


# Create your views here.

# User registration view

class UserRegistration(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = "User %(username)s has been registered"
    success_url = reverse_lazy('login')


#

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


# class ContactDetailsView(LoginRequiredMixin, DetailView):
#     model = Person
#
#     def get_context_data(self, *args, **kwargs):
#         data = super().get_context_data(*args, **kwargs)
#         primary_address = Address.objects.filter(person_id=self.kwargs.get('pk'), type=1)
#         secondary_address = Address.objects.filter(person_id=self.kwargs.get('pk'), type=2)
#         if len(primary_address) != 0:
#             data['primary_address'] = primary_address[0]
#         if len(secondary_address) != 0:
#             data['secondary_address'] = secondary_address[0]
#         return data


class CreateContactView(LoginRequiredMixin, FormSetSuccessMessageMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Person
    form_class = PersonForm
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = ['address_forms', 'phone_forms', 'email_forms', ]
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s created"


class UpdateContactView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_update_form'
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = ['address_forms', 'phone_forms', 'email_forms', ]
    success_message = "Contact %(first_name)s %(last_name)s updated"

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.id,))


class DeleteContactView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)


# Person object mix-in

# class PersonObjectMixin(object):
#     model = Person
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['person_id'] = self.kwargs.get("pk")
#     #     return context
#
#     def get_success_url(self):
#         person_id = self.kwargs.get("pk")
#         return reverse('contact-details', args=(person_id,))


# Address views

# class CreateAddressView(LoginRequiredMixin, CreateView):
#     model = Address
#     fields = '__all__'
#
#     # def form_valid(self, form):
#     #     id = self.kwargs.get(self.pk_url_kwarg)
#     #     self.object = form.save()
#     #     Person.objects.filter(pk=id).update(address=self.object.id)
#     #     return HttpResponseRedirect(self.get_success_url())


# class UpdateAddressView(LoginRequiredMixin, UpdateView):
#     model = Address
#     form_class = AddressForm
#     template_name_suffix = '_update_form'

# def get_object(self):
#     id = self.kwargs.get(self.pk_url_kwarg)
#     object = get_object_or_404(Person, id=id).address_set.all()[0]
#     # TODO check if possible to use 2 pk in url, one for the person, one for the address
#     return object

# def form_valid(self, form):
#     id = self.kwargs.get(self.pk_url_kwarg)
#     self.object = form.save()
#     Person.objects.filter(pk=id).update(address=self.object.id)
#     return HttpResponseRedirect(self.get_success_url())


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Phone views

# class CreatePhoneView(LoginRequiredMixin, CreateView):
#     model = Phone
#     form_class = PhoneForm
#
#     # def form_valid(self, form):
#     #     id = self.kwargs.get(self.pk_url_kwarg)
#     #     self.object = form.save()
#     #     Person.objects.filter(pk=id).update(phone=self.object.id)
#     #     return HttpResponseRedirect(self.get_success_url())
#
#
# class UpdatePhoneView(LoginRequiredMixin, UpdateView):
#     model = Phone
#     form_class = PhoneForm
#     template_name_suffix = '_update_form'
#
#     def get_object(self):
#         id = self.kwargs.get(self.pk_url_kwarg)
#         object = get_object_or_404(Person, id=id).phone
#         # TODO check if possible to use 2 pk in url, one for the person, one for the phone number
#         return object
#
#     def form_valid(self, form):
#         id = self.kwargs.get(self.pk_url_kwarg)
#         self.object = form.save()
#         Person.objects.filter(pk=id).update(phone=self.object.id)
#         return HttpResponseRedirect(self.get_success_url())


class DeletePhoneView(LoginRequiredMixin, DeleteView):
    model = Phone

    def get_success_url(self):
        return reverse_lazy('contact-details', args=(self.object.person_id,))


# Email views

# class CreateEmailView(LoginRequiredMixin, CreateView):
#     model = Email
#     form_class = EmailForm
#
#     def form_valid(self, form):
#         id = self.kwargs.get(self.pk_url_kwarg)
#         self.object = form.save()
#         Person.objects.filter(pk=id).update(email=self.object.id)
#         return HttpResponseRedirect(self.get_success_url())
#
#
# class UpdateEmailView(LoginRequiredMixin, UpdateView):
#     model = Email
#     form_class = EmailForm
#     template_name_suffix = '_update_form'
#
#     def get_object(self):
#         id = self.kwargs.get(self.pk_url_kwarg)
#         object = get_object_or_404(Person, id=id).email
#         # TODO check if possible to use 2 pk in url, one for the person, one for the email
#         return object

# def form_valid(self, form):
#     id = self.kwargs.get(self.pk_url_kwarg)
#     self.object = form.save()
#     Person.objects.filter(pk=id).update(email=self.object.id)
#     return HttpResponseRedirect(self.get_success_url())


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
