# FOODO
#### Video Demo:  https://youtu.be/yof1jDjUU8s
#### Description:
This project is a web based food receipe application and collection
In order to do your groceries for the receipes it includes a handy
to do list app
The application includes a user authentication as it should be not public to everyone once hosted on my own webspace

#### About the web application:
I use a SQLITE database for stroing the recipes and the grocery list

The database gets read, updated, deleted by a pyhton flask backend

frontend design is based on bootstrap 4 (reenginered and extended from cs50 finance)

The application includes following features:
- bright landing page
- receipe overview
- recipe details pages including pictures
- the option to add new recipes
- the option editing existing recipes
- grocery to do list
- and an activity log to keep track of all changes on recipes
- preset filters for "common food"
This project I did especially for my family, I hope they and you enjoy!

The features are represented to the user by following html templates (including a short description)
- add.html                  lets the user add new recipes to the db
- add_todo.html             lets the user add new todos/groceries to the list
- apology.hmtl              serves as error handling screen
- history.html              history of what happened to the recipe db
- index.html                neat landing page
- layout.html               basis for all pages templates layout
- login.html                login screen for user
- recipe_detail.html        shows the selected recipe with all details
- recipe_edit.html          lets the user edit the selected recipe
- recipes.html              list of all existing recipes
- register.html             register option for new user ( disabled once public hosted)
- todo.html                 the grocery/todo overview

#### Technology:
- Frontend:   HTML, CSS
- Backend:    Pyhton Flask Framework
- Database:   SQLITE

#### How to run:
```
$ flask run
```

#### Requirements:
- pyhton 3
- cs50
- Flask
- Flask-Session
- requests


#### Design Background:
the website desgin is drevied from CS50 Finance and based on bootstrap 4
bootstrap is a free frontend design framwork which enables you to design solid webpages
without being a frontend design expert
I recommend the getting started section on w3schools.com
```
https://www.w3schools.com/bootstrap4/bootstrap_get_started.asp
```

#### External Tools
- DB Browser (SQLITE)

```
https://sqlitebrowser.org/
```

this is my favorite tool to "graphically" design backend databases
It easily allows you to create, read, alter, and delete databases/tables and the best is, it
allows you to execute SQL scripts as well against your databases

