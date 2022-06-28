from django.contrib import admin

from contacts_app.models import Person, Address, Phone, Email, Group

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(Group)
