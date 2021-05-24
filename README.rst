NucoroCurrency
==============

NucoroCurrency will be a web platform that allows users to calculate currency
exchange rates.
NucoroCurrency will use an external provider Fixer.io to retrieve and store daily
currency rates. As NucoroCurrency is a flexible platform, it has to be designed to
use multiple currency data providers. So, it won’t only work with Fixer.io but also
with any other providers that might have different APIs for retrieving currency
exchange rates


.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Deployment
----------
The following details how to deploy this application.

Avoid "sudo" With Docker Compose
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To make sure every single working document on project is editable, execute the following commands::

    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    $ sudo service docker restart
    $ gnome-session-quit

Setting Up The Project
^^^^^^^^^^^^^^^^^^^^^

* Build project with docker-compose::

    $ docker-compose -f local.yml build


* Start services::

    $ docker-compose -f local.yml up

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser


* Check database IP (optional)::

    $ docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres_nucoro_currency

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Exercises links & descriptions
------------------------------

Exchange rates data
^^^^^^^^^^^^^^^^^^^

Implementation path
~~~~~~~~~~~~~~~~~~~

* **Models:** ``nucoro_currency/currencies/models.py``

* **External services (fixerio/mock) following "adapter" pattern:** ``nucoro_currency/currencies/utils/``

* **IMPORTANT:** Method 'get_exchange_rate_data' was really confusing to me. To streamline the process in this exercise, I take the name **"get_exchange_rate_by_date"** on clients (Of course, if a real requirement establish this kind of contract, I would never make this option)

Exchange rates API
^^^^^^^^^^^^^^^^^^
**API Root:** http://localhost:8000/api/v1/

**Admin URL:** http://localhost:8000/admin/

Service to retrieve a List of currency rates for a specific time period
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**URL:** http://localhost:8000/api/v1/currency-exchange-rates

Service that Calculates (latest) amount in a currency exchanged into a different currency.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**URL:** http://localhost:8000/api/v1/calculate-exchange

Service to retrieve time-weighted rate of return for any given amount invested from a currency into another one from given date until today:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**URL:** http://localhost:8000/api/v1/twr

At any time you can change Provider priority, to make another one the “default” data source.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Implementation path:** ``nucoro_currency/currencies/signals.py``

Exchange Rate Evolution backoffice / admin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Query param "days" can be changed as desired

**URL:** http://localhost:8000/admin/currencies/dummymodel/exchange-rate-evolution/?days=7

Mechanism to ingest real-ish exchange rate data from a file in any format

**URL:** http://localhost:8000/api/v1/upload-file

Batch procedure to retrieve exchange rates (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This method will process file as async task loading data in DDBB

**URL:** http://localhost:8000/api/v1/upload-file

API versioning / scope (optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
API declared in version "v1"
For a "v2" version you will need add ``config/api_router_v2.py`` with a custom "Router" configuration and  ``path("api/v2/", include("config.api_router_v2")),`` to ``config/urls.py``


To Improve
----------

* Decouple mandatory calls to endpoints in data collections (views)
* According to the previous point, load data to DDBB always asynchronous periodically. In this case, it will be fine add something more to ExchangeRates model like real time rate value (including hour/min), timestamp on creation instance, etc.
* Avoid overwrite "list" method on APIViews, instead use "@action" decorator. This happen because ROOT API does not document correctly "@action" methods
* More documentation and strict typing
* Make some use of testing tools that ensures a minimum coverage of the project
