"""contacts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from contacts.settings import DEBUG
from contacts_app.views import (
    UserRegistration,
    ContactListView, CreateContactView, DeleteContactView, DeleteAddressView,
    DeletePhoneView,
    DeleteEmailView,
    AddContactToGroup,
    GroupListView, GroupDetailView, CreateGroupView, UpdateGroupView, DeleteGroupView,
    UpdateContactView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', UserRegistration.as_view(), name="register"),
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(template_name="users/logged_out.html"), name='logout'),

    path('', ContactListView.as_view(), name="contact-list"),
    path('show/<int:pk>', UpdateContactView.as_view(), name="contact-details"),
    path('new/', CreateContactView.as_view(), name="create-contact"),
    path('delete/<int:pk>', DeleteContactView.as_view(), name="delete-contact"),

    # path('add_address/<int:pk>/', CreateAddressView.as_view(), name="create-address"),
    # path('modify_address/<int:pk>', UpdateAddressView.as_view(), name="update-address"),
    path('delete_address/<int:pk>', DeleteAddressView.as_view(), name="delete-address"),

    # path('add_phone/<int:pk>', CreatePhoneView.as_view(), name="create-phone"),
    # path('modify_phone/<int:pk>', UpdatePhoneView.as_view(), name="update-phone"),
    path('delete_phone/<int:pk>', DeletePhoneView.as_view(), name="delete-phone"),

    # path('add_email/<int:pk>', CreateEmailView.as_view(), name="create-email"),
    # path('modify_email/<int:pk>', UpdateEmailView.as_view(), name="update-email"),
    path('delete_email/<int:pk>', DeleteEmailView.as_view(), name="delete-email"),

    path('add_to_group/<int:pk>', AddContactToGroup.as_view(), name='add-to-group'),

    path('groups/', GroupListView.as_view(), name="group-list"),
    path('groups/show/<int:pk>', GroupDetailView.as_view(), name="group-detail"),
    path('groups/new', CreateGroupView.as_view(), name="create-group"),
    path('groups/modify/<int:pk>', UpdateGroupView.as_view(), name="update-group"),
    path('groups/delete/<int:pk>', DeleteGroupView.as_view(), name="delete-group"),
]

if DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      # url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns
