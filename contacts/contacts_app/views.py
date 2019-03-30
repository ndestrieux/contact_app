from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# from contacts_app.forms import AddressForm
from contacts_app.models import Person, Address, Phone, Email


# Create your views here.


class ContactListView(ListView):
    model = Person

    def get_queryset(self):
        return Person.objects.all().order_by("last_name")


class ContactDetailsView(DetailView):
    model = Person


class CreateContactView(SuccessMessageMixin, CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'description']
    success_url = reverse_lazy('contact-list')
    success_message = "New contact added - %(first_name)s %(last_name)s"


class UpdateContactView(SuccessMessageMixin, UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('contact-list')
    success_message = "Contact %(first_name)s %(last_name)s updated"


class DeleteContactView(SuccessMessageMixin, DeleteView):
    model = Person
    success_url = '/'
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)


class CreateAddressView(CreateView):
    model = Address
    fields = '__all__'

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(address=self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class CreatePhoneView(CreateView):
    model = Phone
    fields = '__all__'

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(phone=self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class CreateEmailView(CreateView):
    model = Email
    fields = '__all__'

    def form_valid(self, form):
        id = self.kwargs.get(self.pk_url_kwarg)
        self.object = form.save()
        Person.objects.filter(pk=id).update(email=self.object.id)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class UpdateAddressView(UpdateView):
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

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class UpdatePhoneView(UpdateView):
    model = Phone
    fields = '__all__'
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

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class UpdateEmailView(UpdateView):
    model = Email
    fields = '__all__'
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

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))
    
    
class DeleteAddressView(DeleteView):
    model = Address
    fields = '__all__'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).address
        return object

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class DeletePhoneView(DeleteView):
    model = Phone
    fields = '__all__'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).phone
        return object

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))


class DeleteEmailView(DeleteView):
    model = Email
    fields = '__all__'

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        object = get_object_or_404(Person, id=id).email
        return object

    def get_success_url(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return reverse('contact-details', args=(id,))
