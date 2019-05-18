# Generated by Django 2.1.7 on 2019-05-12 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('building_number', models.CharField(blank=True, max_length=8, null=True)),
                ('flat_number', models.CharField(blank=True, max_length=8, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Primary'), (2, 'Secondary')])),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=128)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'unknown'), (2, 'work'), (3, 'home')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(to='contacts_app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('type', models.IntegerField(blank=True, choices=[(1, 'unknown'), (2, 'work - stationary'), (3, 'home - stationary'), (4, 'work - mobile'), (5, 'home - mobile')], default=1, null=True)),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts_app.Person')),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts_app.Person'),
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts_app.Person'),
        ),
    ]
