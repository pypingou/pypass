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

   Groups and keys name must never be modified.

   PyPass relies on that exact names to work. If one of groups or keys
   cannot be found, application may not work as excepted or crash.

`global` section
****************

* ``file`` File location: path to the database file you want PyPass opens
  by default.

  * default value: ``~/.pypass/default.asc``
  * possible values: any valid path
* ``recipients``: GPG key used to encode the file by default.

  * default value `(empty)`
  * possible values: any GPG key fingerprint
* ``override_file``: forces the overwrite of the default file if it already
  exists, without asking you.

  * default value: ``False``
  * possible values: ``True`` or ``False``

`password generator` section
****************************

* ``length``: length of the password to generate.

  * default value: ``12``
  * possible values: any positive integer greater than 0
* ``base``: sets the character base to use for password generation.

  * default value: ``1`` (see values below)
  * possible values: from ``0`` to ``5``. Choose one from:

    * ``0``: all printable characters, excluding space::

       !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
    * ``1``: alpha-numeric characters (a-z, A-Z, 0-9)::

       0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
    * ``2``: alpha lower-case characters (a-z)::

       abcdefghijklmnopqrstuvwxyz
    * ``3``: hexadecimal characters (0-9, A-F)::

       0123456789ABCDEF
    * ``4``: decimal characters (0-9)::

       0123456789
    * ``5``: Base 64 (a-z, A-Z, 0-9, +, /)::

       0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/
