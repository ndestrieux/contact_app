from django.db import models


PHONE_TYPE = (
    (1, "NO DATA"),
    (2, "work - stationary"),
    (3, "home - stationary"),
    (4, "work - mobile"),
    (5, "home - mobile")
)

EMAIL_TYPE = (
    (1, "NO DATA"),
    (2, "work"),
    (3, "home")
)


# Create your models here.

class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    building_number = models.CharField(max_length=8, null=True, blank=True)
    flat_number = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return f"{self.street}, nr {self.building_number if self.building_number else '-'}, " \
            f"flat {self.flat_number if self.flat_number else '-'}, {self.city}"


class Phone(models.Model):
    number = models.IntegerField()
    type = models.IntegerField(choices=PHONE_TYPE)

    def __str__(self):
        return f"{self.number} ({PHONE_TYPE[(self.type - 1)][1]})"


class Email(models.Model):
    address = models.CharField(max_length=128)
    type = models.IntegerField(choices=EMAIL_TYPE)

    def __str__(self):
        return f"{self.address} ({EMAIL_TYPE[(self.type - 1)][1]})"


class Group(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.ForeignKey(Phone, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.ForeignKey(Email, null=True, blank=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(Group, null=True, blank=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name
