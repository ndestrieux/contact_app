# CONTACT APP

## How to start

1. [*Fork*](https://guides.github.com/activities/forking/) the project to your profile.
2. [*Clone*](https://help.github.com/articles/cloning-a-repository/) the freshly forked repository on your computer.
3. From postgreSQL interface, run the command `CREATE DATABASE contacts`, the database that the app will interact with will be created.
4. From the repository you just cloned, cd to [git_repository]/contacts and run command `python3 manage.py makemigrations` then `python3 manage.py migrate`.
5. You are ready now to run the app, run the command `python3 manage.py runserver`, the link to reach the app will be showing below.


## App content

* The aim of the app is to manage contacts and assign them an address, a phone number and an email address.
* There is also a group menu, from which you can manage groups. Contact assignment to a group is managed from the contact menu.
* A contact can be created with two addresses maximum, the number of phone numbers or email addresses assigned to a contact is not limited.
* There is also the possibility to display an adress on a map
* Login is required for the use of this app
* Users can only access the content they created
