===============
JUnit Reporting
===============

JUnit Reporting is a simple Django application to facilitate JUnit test report
generation and display.

Quick Start
-----------

1. Add "junit_reporting" as well as "rest_framework" and
   "rest_framework.authtoken to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'rest_framework.authtoken',
        'junit_reporting',
    ]

2. Include the junit_reporting URLconf in your project urls.py like this::

    url(r'^junit_reporting', include('junit_reporting.urls')),

3. Run `python manage.py migrate` to the junit_reporting models.
