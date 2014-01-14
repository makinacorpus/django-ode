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


==========
DEPLOYMENT
==========

Vagrant_ can be used for the deployement. A Vagrantfile is available to easily provision a virtual machine with the frontend and the API inside.

You can change the distribution used by the guest machine by changing the "config.vm.box" and the "config.vm.box_url" option in the Vagrantfile. A list of available images is there: http://www.vagrantbox.es/. The default one is "Ubuntu Server 12.04 amd64 (with Puppet, Chef and VirtualBox 4.2.1)".

We use SaltStack_ to configure the guest. Be sure to use at least the version 1.3.0 of Vagrant.

To create your virtual machine, you must create a pillar. Pillars are used to store sensitive data. An example pillar you can use is available::

    $ cp -R salt/pillar_example salt/pillar

Take a look at the "settings.sls" file inside your pillar and edit it to match your needs. You can now boot up your virtual machine::

    $ vagrant up
    $ vagrant ssh

The applications inside the virtual machine are located in "/home/users/". Virtualenv are created for both of them::

    $ cd /home/users/ode_api/ode/
    $ . ../env/bin/activate

PLEASE READ: We still have issue with the vagrant deployement. The database will not be created and the api will sometimes not be downloaded. For now, you need to manually do::

    $ sudo rm -Rf /home/users/ode_api/ode
    $ sudo salt-call state.sls database
    $ sudo salt-call state.sls apps

The applications are then available on the ports you set in the salt pillar.

To update your virtual machine, you can call salt from the guest. For now, you must also stop the servers manually. It will be fixed in a later release::

    $ cd /home/users/ode_api/ && . env/bin/activate && circusctl stop
    $ cd /home/users/ode_frontend/ && . env/bin/activate && circusctl stop
    $ sudo salt-call state.sls apps


.. _Vagrant: http://www.vagrantup.com/
.. _SaltStack: http://www.saltstack.com/


------------------
SALT CONFIGURATION
------------------

Salt configuration is located in "salt/pillar/settings.sls".

---------------
TROUBLESHOOTING
---------------

TODO

=======
LICENSE
=======

    * BSD New
