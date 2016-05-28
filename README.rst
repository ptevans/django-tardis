=====
Django-Tardis
=====

Tardis puts tooling around freeze_time to allow you to manage "now" in your
application. Set your destination, set stops along the way, and start your trip.
Register callbacks using signals to execute housekeeping code at each stop
during the trip.

Detailed documentation is in the "docs" directory. (TODO)

Quick start
-----------

1. Tardis must be the first app in your INSTALLED_APPS list. Add "polls" to your
INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        'tardis',
        ...
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^tardis/', include('tardis.urls')),

3. Run `python manage.py migrate` to create the tarids models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a trip (you'll need the Admin app enabled).
