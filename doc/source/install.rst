************
Installation
************

.. warning::

   *This is a work in progress.*

   If you have questions about PyPass, you can contact main developers
   joining the `#pypass` :abbr:`IRC (Internet Relay Chat)` channel on the
   `FreeNode <http://freenode.net/>`_ network.

A few words on PyPass
=====================

PyPass relies on GnupPG to encrypt your data. PyPass can store many of you
personal and confidential data, such as
:abbr:`HTTP (HyperText Transfer Protocol)` authentication, OS accounts and so
on. So we'll use your own GPG key to encrypt PyPass' file.

Data are stored in a unique text file, in
:abbr:`JSON (JavaScript Object Notation)` format. Therefore, you can easily
decrypt your file on any computer, without having to install PyPass.

Of course, we advise you to install PyPass, using GnuPG directly won't permit
you to benefit from a beautiful and efficient way to access your data ;-)

.. _prerequisites:

Prerequisites
=============

To run PyPass, you'll need:

* `python <http://python.org>`_ 2.6 or 2.7,
* `python-argparse <http://code.google.com/p/argparse/>`_ (only for python 2.6),
* `pygtk <http://pygtk.org/>`_ (for the :doc:`gui <gtk_gui>` only)
* `python-gnupg <http://code.google.com/p/python-gnupg/>`_,
* `GnuPG <http://www.gnupg.org/>`_ (and your own GPG key).

Python, argparse, pygtk and GnuPG should be available on you distribution,
you'll just have to use your favorite package manager to install them.

As for `python-gnupg`, it is not available on Fedora (14) nor Debian (6) base
repositories. If you use Fedora, there's `a third party repository that
provides python-gnupg package <http://rpms.ulysses.fr>`_.

.. todo::

   find and describe `python-gnupg` installation on Debian like systems

.. _get_the_software:

Get the software
================

PyPass is python software, you will not need to compile anything; just take
the package release, uncompress it, and you're done :-)

.. note::

   Theoretically , all prerequisite software is also available on Windows
   systems, but we do not develop PyPass for such a compatibility for now.

.. _stable_releases:

Stable releases
***************

We will try to have PyPass added in default repositories for some Linux
distributions, but for the moment, there is no package available for it.

As for now, we do not have yet released any PyPass version. You will have to
install :ref:`the development version <development_version>` in order to use it.

.. _development_version:

Development version
*******************

In order to use our development version, you'll need:

* :ref:`standard prerequisites <prerequisites>`,
* `Mercurial <http://mercurial.selenic.com/>`_,

If you plan to build the documentation, you will also need `Sphinx
<http://sphinx.pocoo.org>`_. To get the PDF documentation, you will need
`rst2pdf <http://code.google.com/p/rst2pdf/>`_ (>= 0.16) among with Sphinx.

To get the latest PyPass development version, just clone our Mercurial
 repository:

.. code-block:: bash

   $ hg clone http://hg.ulysses.fr/pypass

No binary nor generated data is available from the sources. If you want to
make translations available or build documentation, you'll have to do it
yourself.

We provide a simple python script to compile translation files, just run the
following command from the `pypass` directory:

.. code-block:: bash

   $ ./pypGetText -c

For the documentation, you will have to use :command:`make` from the `doc`
directory. Just running :command:`make` will show you the possibilities. For
example, to do a clean, and then build documentation in HTML and PDF formats,
you'll have to run:

.. code-block:: bash

   $ make clean html pdf

Results will be available in the `doc/build/html` and/or `build/doc/pdf/`
directories.
Pretty simple, huh? ;-)

Run the software
================

For the moment, there are two ways for using PyPass. In the pypass directory,
you'll find two different scripts:

* ``pypass.py``: command line interface
* ``pypass-gtk.py``: the GTK interface

Of course, if you plan to only use PyPass from command line, you will not have
to install PyGTK.

Those both scripts can take several common options:

* `-D` or `--debug`: to run the program in debug mode,
* `-V` or `--verbose`: cause the software to be a little more verbose,
* `-f` or `--filename`: start PyPass using specified file. If the file does
not exists, PyPass wil start with a new one that will be saved by default
in the location you've specified. Of course, you still can open or save the
file you want from within the interface.

Configuration
=============

PyPass comes with a default configuration file (``pypass/data/pypass.ini``)
that will be loaded first on each startup. User configuration file
(that defaults to ``~/.pypass/pypass.ini``) will be loaded second; and then
the program will take care of command line arguments.

Configuration files are `.ini` python files, in the form::

   [group name]
   key_name = 'value'
   boolean = False

.. todo::

   write config file documentation and add a link here

Please take an eye at the configuration file documentation if want you to learn
more on available options, their values, and most important: possible values.