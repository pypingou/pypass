**********************
Command line interface
**********************


Simple commands
===============

In order to use PyPass command line interface, you just have to use provided
``pypass.py`` script.

To get the complete list of available commands, just run:

.. code-block:: bash

   $ ./pypass.py -h

You can get the entire list using `--list` (or `-l`) flag:

.. todo:: That example is from a development version that doe not work as expected

.. code-block:: bash

   $ ./pypass.py --list
   Folders:
     PyPass
     Fedora

Interactive mode
================

To enter interactive mode, use the `--interactive` (or `-i`) flag. If you want
to get help while using the interactive mode, just type `help`:

.. code-block:: bash

   $ ./pypass.py --interactive
   (Cmd) help

   Undocumented commands:
   ======================
   exit  help  ls  pwd

   (Cmd) ls
   Folders:
     PyPass
     Fedora
   (Cmd) pwd
   We do not knonw yet.
   (Cmd) exit
