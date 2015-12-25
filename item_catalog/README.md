# Item Catalog
Web application that provides a list of items within a variety of categories and integrate third party user registration and authentication (OAuth). Authenticated users have the ability to post, edit, and delete their own items.

The current implementation of the item catalog is a restaurant catalog that provides a list of restaurants and their menus.

## View the app online

You can view the app online [here](https://warm-reaches-9715.herokuapp.com/).

## Run the app in your browser

To run the app in your browser you need install python first.

Once python is installed install the following dependencies with pip:

```
pip install Flask sqlalchemy oauth2client
```

## Set up the database

To create the database open a terminal and run:

`python setup.py`

This will create the database **restaurantsdb**.

## Populate the database

To populate the database with a list of restaurants run:

`python populate.py`

## Run the server

To run the server type the following:

`python restaurants.py`

and visit [0.0.0.0:5000](0.0.0.0:5000) or [localhost:5000](localhost:5000) in your browser.
