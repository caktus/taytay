Taytay Quick Start
====================================

Below you will find basic setup and deployment instructions for the taytay
project. To begin you should have the following applications installed on your
local development system:

- Python >= 3.4
- `pip <http://www.pip-installer.org/>`_ >= 1.5
- `virtualenv <http://www.virtualenv.org/>`_ >= 1.10
- `virtualenvwrapper <http://pypi.python.org/pypi/virtualenvwrapper>`_ >= 3.0
- Postgres >= 9.3
- git >= 1.7


Getting Started
---------------

First clone the repository from Github and switch to the new directory::

    $ git clone git@github.com:[ORGANIZATION]/taytay.git
    $ cd taytay

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    # Check that you have python3.4 installed
    $ which python3.4
    $ mkvirtualenv taytay -p `which python3.4`
    (taytay)$ make dev

Configurable settings are managed with `django-dotenv <https://github.com/jpadilla/django-dotenv>`_.
It reads environment variables located in a file name ``.env`` in the top level directory of the project.
The previous command ``make dev`` creates new ``.env`` file with a new ``SECRET_KEY`` value set.

Create the Postgres database and run the initial migrate::

    (taytay)$ createdb -E UTF-8 taytay
    (taytay)$ python manage.py migrate

You should now be able to run the development server::

    (taytay)$ python manage.py runserver

Connecting to the API
---------------------

To connect to the API at baelor.io, you'll need to create a user using the
following curl command ::

    $ curl -H "Content-Type: application/json" -X POST -d
    '{"username": "yourusername","email_address": "youremail",
    "password": "yourpassword","password_confirm": "yourpassword"}'
    http://baelor.io/api/v0/users

You should receive an API key in the response. To make use of this key, you should
include it in your ``.env`` file::

    $ echo 'BAELOR_API_KEY="<api key>"' >> .env

Where ``<api key>`` would be replaced with your actual API key value.


Testing
-------

The ``Makefile`` for this project has a number of helpful commands for testing
and checking code quality. Below is a brief description of the commands

- ``make test`` - Runs the full test suite and reports test coverage
- ``make lint`` - Runs a set of subcommands to check code quality

 - ``make lint-py`` - Runs the code through ``flake8`` for static analysis
 - ``make lint-migrations`` - Runs Django's checks for model changes without migrations
 - ``make lint-django`` - Runs Django's system checks with the base settings
 - ``make lint-deploy`` - Runs Django's system checks for deployment
