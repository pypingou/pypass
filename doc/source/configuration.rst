*************
Configuration
*************

.. warning::

   *This is a work in progress.*

PyPass comes with a default configuration file (``pypass/data/pypass.ini``)
that will be loaded first on each startup. User configuration file
(that defaults to ``~/.pypass/pypass.ini``) will be loaded second; and then
the program will take care of command line arguments.

Configuration files are `.ini` python files, in the form::

   [group name]
   key_name = 'value'
   boolean = False

Take an eye at the configuration file documentation below if want you to know
available options, default and possible values.

The configuration file
======================

.. warning::

   Groups and keys name must never be modified. The program relies on that
   names to work. If one of groups or keys cannot be found, application may
   crash.

.. todo::

   describe config file documentation
