django-ode
==========

.. image:: https://travis-ci.org/makinacorpus/django-ode.png
    :target: https://travis-ci.org/makinacorpus/django-ode

.. image:: https://coveralls.io/repos/makinacorpus/django-ode/badge.png
    :target: https://coveralls.io/r/makinacorpus/django-ode


=======
AUTHORS
=======

|makinacom|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com


===========
DEVELOPMENT
===========

We provide a ``Makefile`` with a few useful targets for development.

To install the app in development mode (you should probably do this in a `virtual environment <http://www.virtualenv.org>`_)::

    $ make develop

To run the test suite::

    $ make test
    $ make coverage

We also provide a management command to create an admin user::

    $ python manage.py create_admin --username=bob --password=s3cr3t


=======
LICENSE
=======

    * BSD New
