# CONTACT APP

## How to start

1. [*Fork*](https://guides.github.com/activities/forking/) the project to your profile.
2. [*Clone*](https://help.github.com/articles/cloning-a-repository/) the freshly forked repository on your computer.
3. Create a .env file at the base of the project repository, in which you'll have to set the variables below:
       <details>
       <summary>see .env file variables</summary>
        SECRET_KEY<br>
        DEBUG<br>
        DATABASE_NAME<br>
        DATABASE_USER<br>
        DATABASE_PASSWORD<br>
        DATABASE_HOST<br>
        </details>
4. At the base of the project repository run the command in a terminal: `docker compose up --build -d`.
5. Once the app has started, open [localhost](http://localhost/) in a web browser.


## App content

* The aim of the app is to manage contacts and assign them an address, a phone number and an email address.
* There is also a group menu, from which you can manage groups. Contact assignment to a group is managed from the contact menu.
* A contact can be created with two addresses maximum, the number of phone numbers or email addresses assigned to a contact is not limited.
* There is also the possibility to display an address on a map
* Login is required for the use of this app
* Users can only access the content they created
