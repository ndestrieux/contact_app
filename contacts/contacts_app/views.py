from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from contacts_app.forms import PersonForm, PhoneForm, EmailForm, ContactGroupForm
from contacts_app.models import Person, Address, Phone, Email, Group


# Create your views here.

# Person views

class ContactListView(ListView):
    model = Person
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return (Person.objects.filter(first_name__icontains=search)
                | Person.objects.filter(last_name__icontains=search))\
            .order_by("last_name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['search'] = self.request.GET.get('search')
        return data


class ContactDetailsView(DetailView):
    model = Person


class CreateContactView(SuccessMessageMixin, CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('contact-list')
    success_message = "New contact added - %(first_name)s %(last_name)s"


class UpdateContactView(SuccessMessageMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s updated"


class DeleteContactView(SuccessMessageMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)

    # TODO find a way to delete foreign keys with, it otherwise find to manage them


# Person object mix-in

class PersonObjectMixin(object):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_id'] = self.kwargs.get("pk")
        return context

    def get_success_url(self):
        person_id = self.kwargs.get("pk")
        return reverse('contact-details', args=(person_id,))


# Address views

class CreateAddressView(PersonObjectMixin, CreateView):
    model = Address
    fields = '__all__'

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(address=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class UpdateAddressView(PersonObjectMixin, UpdateView):
    model = Address
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).address
        return object

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(address=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class DeleteAddressView(PersonObjectMixin, DeleteView):
    model = Address

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).address
        return object


# Phone views

class CreatePhoneView(PersonObjectMixin, CreateView):
    model = Phone
    form_class = PhoneForm

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(phone=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class UpdatePhoneView(PersonObjectMixin, UpdateView):
    model = Phone
    form_class = PhoneForm
    template_name_suffix = '_update_form'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).phone
        return object

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(phone=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class DeletePhoneView(PersonObjectMixin, DeleteView):
    model = Phone

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).phone
        return object


# Email views

class CreateEmailView(PersonObjectMixin, CreateView):
    model = Email
    form_class = EmailForm

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(email=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class UpdateEmailView(PersonObjectMixin, UpdateView):
    model = Email
    form_class = EmailForm
    template_name_suffix = '_update_form'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).email
        return object

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(email=self.object.id)
        return HttpResponseRedirect(self.get_success_url())


class DeleteEmailView(PersonObjectMixin, DeleteView):
    model = Email

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).email
        return object


class AddContactToGroup(PersonObjectMixin, UpdateView):
    model = Person
    form_class = ContactGroupForm
    template_name = 'contacts_app/add_contact_to_group.html'


# Group views

class GroupListView(ListView):
    model = Group

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return Group.objects.filter(name__icontains=search).order_by("name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['search'] = self.request.GET.get('search')
        return data


class GroupDetailView(DetailView):
    model = Group


class CreateGroupView(SuccessMessageMixin, CreateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('group-list')
    success_message = "New group added - %(name)s"


class UpdateGroupView(SuccessMessageMixin, UpdateView):
    model = Group
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s updated"


class DeleteGroupView(SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group-list')
    success_message = "Group %(name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteGroupView, self).delete(request, *args, **kwargs)
