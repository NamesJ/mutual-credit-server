# mutual-credit-server
A mutual credit system implemented as a REST API server

# Disclaimer
This project is not yet ready for production use... but it's getting there.

# Current state of this project
The requirements for this project are (roughly):
* User authentication (register, login, recovery, etc.)
  * Email-based registration
    * Basic email based authentication is implemented
    * No email verification process implemented yet
  * User registration and login
    * Working and with unit tests
  * Token-based authentication
    * Fully-implemented (thanks to Flask-JWT-Extended)
  * Discord-based registration :)
    * Discords community-based user management and extensive API mean that it could serve as an alternative to email in this case.
    * Reflecting user roles from Discord into mutual credit server for assigning and managing permissions
    * Direct Messaging from bot to server members for notifications and account recover (email stuff)
* Credit System
  * Transfers (create, cancel, deny, approve)
    * Working and with a good deal of unit tests

# Features
* Full featured API framework with [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
* Swagger Documentation (Part of Flask-RESTX).
* JSON Web Token Authentication with [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)
* Unit Testing with [unittest](https://docs.python.org/3/library/unittest.html).
* Database ORM with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* Database Migrations using [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate)
* Object serialization/deserialization with [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* Data validations with Marshmallow [Marshmallow](https://marshmallow.readthedocs.io/en/stable/quickstart.html#validation)

## A very special thanks to `X1Zeth2X` for their flask-restx boilerplate
Their code was extremely helpful in getting this project off the ground (and keeping the monolith from suffocating it to death). Check out their project [here](https://github.com/X1Zeth2X/flask-restx-boilerplate).

## Flask CLI help command output:
```sh
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
  test    Run unit tests
```

# Pre-requisites

This boilerplate uses `SQLite` as its database, make sure you have it installed.
`Pipenv` is recommended to help manage the dependencies and virtual environment. You can read more about it [here](https://pypi.org/project/pipenv/])

You can also use other DBs like `PostGreSQL`, make sure you have it setup and update your `DATABASE_URL` in your configs.
Read more at [Flask-SQLAlchemy's](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) documentations.

# Usage

## Notes

By default the `/` route is used by the `auth` blueprint.

The rest of the resources are found in `/api`

## Installing
```sh
# Clone the repo
$ git clone https://github.com/NamesJ/mutual-credit-server

# Install packages from Pipfile.lock with pipenv (RECOMMENDED)
$ pipenv install --ignore-pipfile

# -- OR --

# Install packages from Pipfile and update Pipfile.lock (NOT RECOMMENDED)
$ pipenv install
```

## Running
Please specify your app's environment variables in a `.env` file, otherwise Flask CLI wouldn't find your app.

```sh
# .env file example

# .env for development (RECOMMENDED)
# Make a copy of the development.env
$ cp development.env .env

# -- OR --

export FLASK_APP=mcs

# configs: production, testing, development, and default (uses DevelopmentConfig)
export FLASK_CONFIG=development

# -- OR --

# Another way of assigning environment variables is:
FLASK_APP=mcs
FLASK_CONFIG=development

# Read more at https://github.com/theskumar/python-dotenv
```

```sh
# Enter the virtualenv
$ pipenv shell

# Run the app
$ flask run
```

# API Documentation
Thanks to Flask-RESTX, this project has swagger documentation. After calling `flask run` just point your web browser to the blueprint that you would like to see documentation for.
As an example, the default address is 'http://127.0.0.1:5000/', and the blueprint for all non-authentication related operations (i.e. for interacting with transfers) is `/api`. So, to see the documentation for the `api` blueprint simply point your browser to `http://127.0.0.1:5000/api/` to view the documentation as a webpage provided by flask-restx.

## Unit testing
Mutual Credit Server has some unit tests written, which you can find in the `tests` package.

```sh
# Running tests

# Unit testing (all tests)
$ flask test

# Run specific unit test(s)
$ flask test tests.test_user_model tests.test_transfer_api ...
```
