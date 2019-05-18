from django.contrib import admin

# Register your models here.
from contacts_app.models import Person, Address, Phone, Email

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Email)
