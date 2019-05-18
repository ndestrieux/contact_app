from django.core.management.base import BaseCommand
from contacts_app.models import Person, Address, Phone, Email, Group


class Command(BaseCommand):
    help = 'Populates contacts with addresses, phones, emails and groups'

    def handle(self, *args, **options):
        # Create address
        a1 = Address.objects.create(city="Los Angeles", street="Mulholland Drive", building_number="666")
        a2 = Address.objects.create(city="Twin Peaks", street="Horror street",
                                    building_number="7", flat_number="1")
        a3 = Address.objects.create(city="Twin Peaks", street="Horror street",
                                    building_number="7", flat_number="1b")
        a4 = Address.objects.create(city="Washington", street="Pennsylvania Avenue", building_number="935")
        a5 = Address.objects.create(city="Los Angeles", street="Hollywood Boulevard", building_number="1876c")

        # Create phone number
        ph1 = Phone.objects.create(number="123456789", type=2)
        ph2 = Phone.objects.create(number="656789123", type=2)
        ph3 = Phone.objects.create(number="689123456", type=5)
        ph4 = Phone.objects.create(number="234567891", type=4)
        ph5 = Phone.objects.create(number="345678912", type=5)

        # Create email address
        em1 = Email.objects.create(address="horror_house@mail.com", type=2)
        em2 = Email.objects.create(address="slee@mail.com", type=3)
        em3 = Email.objects.create(address="rwise@mail.com", type=3)
        em4 = Email.objects.create(address="maclachlan@fbi.com", type=2)
        em5 = Email.objects.create(address="tburton@mail.com", type=3)

        # Create groups
        g1 = Group.objects.create(name="Twin Peaks")
        g2 = Group.objects.create(name="Solitary group")

        # Create people
        p1 = Person.objects.create(first_name="David", last_name="Lynch", address=a1, phone=ph1, email=em1)
        p2 = Person.objects.create(first_name="Robert", last_name="Engels", address=a1, phone=ph1, email=em1)
        p3 = Person.objects.create(first_name="Sheryl", last_name="Lee", address=a2, phone=ph2, email=em2)
        p4 = Person.objects.create(first_name="Ray", last_name="Wise", address=a3, phone=ph3, email=em3)
        p5 = Person.objects.create(first_name="Kyle", last_name="MacLachlan",
                                   description="FBI agent", address=a4, phone=ph4, email=em4)
        p6 = Person.objects.create(first_name="Tim", last_name="Burton", address=a5, phone=ph5, email=em5)

        p1.groups.add(g1)
        p2.groups.add(g1)
        p3.groups.add(g1)
        p4.groups.add(g1)
        p5.groups.add(g1)
        p6.groups.add(g2)
