django-ode
==========

.. image:: https://travis-ci.org/makinacorpus/django-ode.png?branch=master
    :target: https://travis-ci.org/makinacorpus/django-ode

.. image:: https://coveralls.io/repos/makinacorpus/django-ode/badge.png?branch=master
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

To run the test suite under against both Python 2 and Python 3, use tox::

    $ tox

We also provide a management command to create an admin user::

    $ python manage.py create_admin --username=bob --password=s3cr3t


==========
DEPLOYMENT
==========

Vagrant VM
----------

Vagrant_ can be used for the deployement. A Vagrantfile is available to easily provision a virtual machine with the frontend and the API inside.

You can change the distribution used by the guest machine by changing the "config.vm.box" and the "config.vm.box_url" option in the Vagrantfile. A list of available images is there: http://www.vagrantbox.es/.

We use SaltStack_ to configure the guest. Be sure to use at least the version 1.3.0 of Vagrant.

To create your virtual machine, you must create a pillar. Pillars are used to store sensitive data. An example pillar you can use is available::

    $ cp -R salt/pillar_example salt/pillar

Take a look at the "settings.sls" file inside your pillar and edit it to match your needs. You can now boot up your virtual machine::

    $ vagrant up
    $ vagrant ssh

The applications inside the virtual machine are located in "/home/users/". Virtualenv are created for both of them::

    $ cd /home/users/ode_api/ode/
    $ . ../env/bin/activate

PLEASE READ: We still have issue with the vagrant deployement. The database
may not get created. You may need to manually do::

    $ sudo salt-call state.sls database

The applications are then available on the ports you set in the salt pillar.

To update your virtual machine, you can call salt from the guest. For now, you must also stop the servers manually. It will be fixed in a later release::

    $ cd /home/users/ode_api/ && . env/bin/activate && circusctl stop
    $ cd /home/users/ode_frontend/ && . env/bin/activate && circusctl stop
    $ sudo salt-call state.sls apps


.. _Vagrant: http://www.vagrantup.com/
.. _SaltStack: http://www.saltstack.com/


Production
----------

TODO

------------------
SALT CONFIGURATION
------------------

SaltStack configuration is located in "salt/pillar/settings.sls".

The different states are located in "salt/roots/". The applications themselves are provisionned by the "apps" state.
Pyramid configuration file (used by the api) is located in "salt/roots/apps/production.ini".
Django configuration file (used by the frontend) is located in "salt/roots/apps/local_settings.py".
Circus configuration file (used to monitor the api's and frontend's wsgi) is located in "salt/roots/apps/circus.ini".


---------------
TROUBLESHOOTING
---------------

If the virtual machines is not provisionned at all, check if you have at least the 1.3.0 version of Vagrant. Else you can manually install the SaltStack plugin::

    $ vagrant plugin install vagrant-salt

=======
LICENSE
=======

    * BSD New
