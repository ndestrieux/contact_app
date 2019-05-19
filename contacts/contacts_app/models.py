from django.db import models
from django_countries.fields import CountryField
from folium import Map, Marker, Icon
from geopy import Nominatim


ADDRESS_TYPE = (
    (1, "Primary"),
    (2, "Secondary")
)

PHONE_TYPE = (
    (1, "unknown"),
    (2, "work - stationary"),
    (3, "home - stationary"),
    (4, "work - mobile"),
    (5, "home - mobile")
)

EMAIL_TYPE = (
    (1, "unknown"),
    (2, "work"),
    (3, "home")
)


class Group(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    groups = models.ManyToManyField(Group)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_primary_address(self):
        return self.address_set.filter(type="1")

    def get_secondary_address(self):
        return self.address_set.filter(type="2")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['first_name', 'last_name', ]


class Address(models.Model):
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    building_number = models.CharField(max_length=8, null=True, blank=True)
    flat_number = models.CharField(max_length=8, null=True, blank=True)
    type = models.IntegerField(choices=ADDRESS_TYPE)
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def full_address(self):
        return f"{self.street}, {'nr ' + self.building_number + ', ' if self.building_number else ''}" \
            f"{'flat ' + self.flat_number + ', ' if self.flat_number else ''} {self.city} - {self.country.name}"

    def get_map(self):
        location = f"{self.street} {self.building_number if self.building_number else ''} " \
            f"{self.city} {self.country.name}"
        loc = Nominatim().geocode(location)
        latlng = [loc.latitude, loc.longitude]
        address_map = Map(location=latlng, zoom_start=18)
        address_map.add_child(Marker(location=latlng, popup=loc.address, icon=Icon(color='red')))
        return address_map._repr_html_()

    def __str__(self):
        return self.full_address

    class Meta:
        unique_together = ['person', 'type', ]


class Phone(models.Model):
    number = models.IntegerField()
    type = models.IntegerField(choices=PHONE_TYPE, default=1, blank=True, null=True)
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number}"


class Email(models.Model):
    address = models.CharField(max_length=128)
    type = models.IntegerField(choices=EMAIL_TYPE, default=1, blank=True, null=True)
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}"

