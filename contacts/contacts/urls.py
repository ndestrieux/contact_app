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
from django.urls import path

from contacts.settings import DEBUG
from contacts_app.views import ContactListView, ContactDetailsView, CreateContactView, UpdateContactView, \
    DeleteContactView, CreateAddressView, CreatePhoneView, CreateEmailView, UpdateAddressView, UpdatePhoneView, \
    UpdateEmailView, DeleteAddressView, DeletePhoneView, DeleteEmailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', ContactListView.as_view(), name="contact-list"),
    path('show/<int:pk>', ContactDetailsView.as_view(), name="contact-details"),
    path('new/', CreateContactView.as_view(), name="create-contact"),
    path('modify/<int:pk>', UpdateContactView.as_view(), name="update-contact"),
    path('delete/<int:pk>', DeleteContactView.as_view(), name="delete-contact"),

    path('<int:pk>/add_address', CreateAddressView.as_view(), name="create-address"),
    path('<int:pk>/add_phone', CreatePhoneView.as_view(), name="create-phone"),
    path('<int:pk>/add_email', CreateEmailView.as_view(), name="create-email"),

    path('<int:pk>/modify_address', UpdateAddressView.as_view(), name="update-address"),
    path('<int:pk>/modify_phone', UpdatePhoneView.as_view(), name="update-phone"),
    path('<int:pk>/modify_email', UpdateEmailView.as_view(), name="update-email"),

    path('<int:pk>/delete_address', DeleteAddressView.as_view(), name="delete-address"),
    path('<int:pk>/delete_phone', DeletePhoneView.as_view(), name="delete-phone"),
    path('<int:pk>/delete_email', DeleteEmailView.as_view(), name="delete-email"),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
