# DJANGO_WARSZTATY_SAMODZIELNE - COTACT BOX
Coders Lab - W02 - Warsztaty Django samodzielne

#### Requirements:
* python3==3.7
* Django==2.1.7
* django-crispy-forms==1.7.2
* django-debug-toolbar==1.11
* psycopg2-binary==2.7.7
* pytz==2018.9


## How to start

1. [*Fork*](https://guides.github.com/activities/forking/) the project to your profile.
2. [*Clone*](https://help.github.com/articles/cloning-a-repository/) the freshly forked repository on your computer.
3. From postgreSQL interface, run the command `CREATE DATABASE contacts`, the database that the app will interact with will be created.
4. From the repository you just cloned, cd to [git_repository]/contacts and run command `python3 manage.py makemigrations` then `python3 manage.py migrate`.
5. (Optional) You have the possibility to populate your contact database for testing purposes by running the command `python manage.py populatecontacts`
6. You are ready now to run the app, run the command `python3 manage.py runserver`, the link to reach the app will be showing below.


## App content

* The aim of the app is to manage contacts and assign them an address, a phone number and an email address.
* There is also a group menu, from which you can manage groups. Contact assignment to a group is managed from the contact menu.
* Once a new contact is created, go to contact details (by clicking on the first name of the contact) from the main view to assign him an address, phone, email and group.
