# Generated by Django 3.2 on 2022-05-31 13:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='person',
            unique_together={('first_name', 'last_name', 'created_by')},
        ),
    ]
