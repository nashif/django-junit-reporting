===============
JUnit Reporting
===============

JUnit Reporting is a simple Django application to facilitate JUnit test report
generation and display.

Requirements
------------

JUnit Reporting requires the following libraries and applications:

1. `Django REST framework <http://www.django-rest-framework.org/>`_
2. `junitparser <https://pypi.python.org/pypi/junitparser>`_
3. `django-font-awesome <https://pypi.python.org/pypi/django-font-awesome>`_
4. `django-bootstrap3 <https://pypi.python.org/pypi/django-bootstrap3>`_
5. `django-static-precompiler <https://pypi.python.org/pypi/django-static-precompiler>`_
6. `django-autoslug <https://pypi.python.org/pypi/django-autoslug>`_

In addition to these Python dependencies, JUnit Reporting also needs
`less.js <https://www.npmjs.com/package/less>`_ to compile its style sheets.

Installing
----------

JUnit Reporting is currently not available in the PyPI since it is still very
volatile. You can however install JUnit Reporting using pip and this git
repository:

.. code-block:: sh

  $ pip install git+https://github.com/fmorgner/django-junit-reporting

Getting Started
---------------

1. Add "junit_reporting" as well as its dependencies to your `INSTALLED_APPS`
   setting like so:

.. code-block:: python

  INSTALLED_APPS = [
      #  other applications ...
      'bootstrap3',
      'font_awesome',
      'junit_reporting',
      'rest_framework',
      'rest_framework.authtoken',
      'static_precompiler',
  ]

2. Include the junit_reporting `URLconf` in your project `urls.py` like this:

.. code-block:: python

  from django.conf.urls import include
  #  ...
  urlpatterns = [
    #  other URLs ...
    url(r'^reporting', include('junit_reporting.urls')),
  ]

3. Make sure to include the static precompiler as a `STATICFILES_FINDERS` entry
   and ensure you have set you `STATIC_ROOT`, similar to this:

.. code-block:: python

  STATICFILES_FINDERS = (
      'django.contrib.staticfiles.finders.FileSystemFinder',
      'django.contrib.staticfiles.finders.AppDirectoriesFinder',
      'static_precompiler.finders.StaticPrecompilerFinder',
  )

  STATIC_URL = '/static/'

  STATIC_ROOT = os.path.join(BASE_DIR, 'static')

4. Enable token authorization in Django REST framework:

.. code-block:: python

  REST_FRAMEWORK = {
      'DEFAULT_PERMISSION_CLASSES': (
          'rest_framework.permissions.IsAuthenticated',
      ),
      'DEFAULT_AUTHENTICATION_CLASSES': (
          'rest_framework.authentication.TokenAuthentication',
      )
  }

5. Run `python manage.py migrate` to install the JUnit Reporting models.

In order to start publishing test reports, you will need to create a user and at
least one project. Currently, you can do this either using the Django python
shell, or via the Django admin interface.

Demo
----

A working demo can be found at the `ARKNet reporting <https://reporting.arknet.ch>`_
site.
