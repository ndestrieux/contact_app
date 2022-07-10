from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.views import PasswordChangeView
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView

from contacts_app.forms import (
    PersonForm,
    UserRegistrationForm,
    PhoneFormSet,
    EmailFormSet,
    AddressFormSet,
    UpdateGroupForm,
)
from contacts_app.models import Person, Address, Phone, Email, Group


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_message = "User %(username)s has been registered"
    success_url = reverse_lazy("login")


class PwChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("contact-list")
    success_message = "Password updated"


class UserAccessMixin:
    def get_queryset(self):
        get_object_or_404(
            self.model, id=self.kwargs.get("pk"), created_by=self.request.user
        )
        return super().get_queryset()


class ContactListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10

    def get_queryset(self):
        current_user_person_query = Person.objects.filter(created_by=self.request.user)
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return (
            current_user_person_query.filter(first_name__icontains=search)
            | current_user_person_query.filter(last_name__icontains=search)
        ).order_by("last_name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["search"] = self.request.GET.get("search")
        return data


class CreateContactView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    NamedFormsetsMixin,
    CreateWithInlinesView,
):
    model = Person
    form_class = PersonForm
    inlines = [
        AddressFormSet,
        PhoneFormSet,
        EmailFormSet,
    ]
    inlines_names = [
        "address_forms",
        "phone_forms",
        "email_forms",
    ]
    success_url = reverse_lazy("contact-list")
    success_message = "Contact %(first_name)s %(last_name)s created"


class UpdateContactView(
    LoginRequiredMixin,
    UserAccessMixin,
    SuccessMessageMixin,
    NamedFormsetsMixin,
    UpdateWithInlinesView,
):
    model = Person
    form_class = PersonForm
    template_name_suffix = "_update_form"
    inlines = [AddressFormSet, PhoneFormSet, EmailFormSet]
    inlines_names = [
        "address_forms",
        "phone_forms",
        "email_forms",
    ]
    success_message = "Contact %(first_name)s %(last_name)s updated successfully"

    def get_success_url(self):
        return reverse_lazy("contact-details", args=(self.object.id,))


class DeleteContactView(LoginRequiredMixin, UserAccessMixin, SuccessMessageMixin, DeleteView):
    model = Person
    success_url = reverse_lazy("contact-list")
    success_message = "Contact %(first_name)s %(last_name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)


class AddressDetailView(LoginRequiredMixin, UserAccessMixin, DetailView):
    model = Address


class DeleteAddressView(LoginRequiredMixin, UserAccessMixin, DeleteView):
    model = Address

    def get_success_url(self):
        return reverse_lazy("contact-details", args=(self.object.person_id,))


class DeletePhoneView(LoginRequiredMixin, UserAccessMixin, DeleteView):
    model = Phone

    def get_success_url(self):
        return reverse_lazy("contact-details", args=(self.object.person_id,))


class DeleteEmailView(LoginRequiredMixin, UserAccessMixin, DeleteView):
    model = Email

    def get_success_url(self):
        return reverse_lazy("contact-details", args=(self.object.person_id,))


class GroupListView(LoginRequiredMixin, UserAccessMixin, ListView):
    model = Group
    paginate_by = 10

    def get_queryset(self):
        # Avoid current logged user from accessing data from other users
        current_user_group_query = Group.objects.filter(created_by=self.request.user)
        # Search engine for groups
        search = self.request.GET.get("search")
        if search is None:
            search = ""
        return current_user_group_query.filter(name__icontains=search).order_by("name")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["search"] = self.request.GET.get("search")
        return data


class GroupDetailView(LoginRequiredMixin, UserAccessMixin, DetailView):
    model = Group


class CreateGroupView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Group
    fields = [
        "name",
        "description",
    ]
    success_url = reverse_lazy("group-list")
    success_message = "New group added - %(name)s"


class UpdateGroupView(LoginRequiredMixin, UserAccessMixin, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = UpdateGroupForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("group-list")
    success_message = "Group %(name)s updated"

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        member_list = Person.objects.filter(
            groups=self.object.id, created_by=self.request.user
        ).values_list("pk", flat=True)
        initial["members"] = member_list
        return initial

    def form_valid(self, form):
        for m_id in form.cleaned_data["members"].values_list("pk", flat=True):
            m = Person.objects.get(id=m_id)
            m.groups.add(self.object.id)
        return super().form_valid(form)


class DeleteGroupView(LoginRequiredMixin, UserAccessMixin, SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy("group-list")
    success_message = "Group %(name)s deleted"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)
