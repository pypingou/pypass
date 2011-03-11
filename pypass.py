#!/usr/bin/python
#-*- coding: utf-8 -*-

# Copyright (c) 2011 Pierre-Yves Chibon <pingou AT pingoured DOT fr>
# Copyright (c) 2011 Johan Cwiklinski <johan AT x-tnd DOT be>
#
# This file is part of pypass.
#
# pypass is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pypass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pypass.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import cmd
import gettext
import sys

from pypass import pyp
from pypass import __version__, __application__
from pypass import __description__, __locale_dir__

gettext.install(__application__, __locale_dir__)


class PyPassInteractive(cmd.Cmd):

    def __init__(self, pyp, filename=None):
        cmd.Cmd.__init__(self)
        self.pyp = pyp
        self.filename = filename

    def do_echo(self, params):
        print params

    def do_pwd(self, params):
        print 'We do not knonw yet.'

    def do_ls(self, params):
        self.pyp.load_data(filename=self.filename)
        if self.pyp.data is not None and self.pyp.data != "":
            pyp_main_folder = self.pyp.json_to_tree()

            if len(pyp_main_folder.folders) > 0:
                print _("Folders:")
                for folder in pyp_main_folder.folders:
                    print "  " + folder.name

            if len(pyp_main_folder.accounts) > 0:
                print _("Accounts:")
                for account in pyp_main_folder.accounts:
                    print account


    def do_exit(self, params):
        sys.exit(1)


class PyPassCli(object):

    def __init__(self, pypass):
        self.pyp = pypass
        self.parseArgs()

    def parseArgs(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description=__description__,
                                         version="%(name)s %(version)s" %
                              {'name': __application__,
                               'version': __version__})

        group = parser.add_argument_group(_('Common options'))
        group.add_argument('-f',
                           '--file',
                           dest='filename',
                           help=_('The accounts database file, this override '\
                                  'the default value'))
        group.add_argument('-V',
                           '--verbose',
                           dest='verbose',
                           help=_('Be a bit more verbose.'),
                           action='store_true',
                           default=False)
        group.add_argument('-D',
                           '--debug',
                           dest='debug',
                           help=_('Activate debug mode (show executed '\
                                  'commands, etc.).'),
                           action='store_true',
                           default=False)

        exclusive_query_group = parser.add_mutually_exclusive_group(required = True)
        exclusive_query_group.add_argument('-l',
                                 '--list',
                                 help=_('List folders'),
                                 nargs='?',
                                 default='')
        exclusive_query_group.add_argument('-g',
                                 '--get',
                                 help=_('Retrieve an account by its ID'),
                                 action='store',
                                 nargs='+',
                                 default=False)

        exclusive_query_group.add_argument('-i',
                                   '--interactive',
                                   help=_('Enter PyPass interactive mode'),
                                   action='store_true',
                                   default=False)

        args = parser.parse_args()

        if args.debug:
            #TODO: init a debug mode
            pass
        if args.verbose:
            #TODO: init a verbose mode
            pass

        if not args.filename:
            args.filename = None

        #List mode
        if args.list != '':
            #TODO: the --list option should show the entire tree, interactive
            #mode should be used to be more concise.
            self.pyp.load_data(filename=args.filename)
            if self.pyp.data is not None and self.pyp.data != "":
                pyp_main_folder = self.pyp.json_to_tree()

                if args.list != None:
                    print pyp_main_folder.folders

                if len(pyp_main_folder.folders) > 0:
                    print _("Folders:")
                    for folder in pyp_main_folder.folders:
                        print "  " + folder.name

                if len(pyp_main_folder.accounts) > 0:
                    print _("Accounts:")
                    for account in pyp_main_folder.accounts:
                        print account

        #Retrieve mode
        if args.get:
            #TODO: what to do if mulitple ids can match?
            pass

        #Interactive mode
        if args.interactive:
            PyPassInteractive(self.pyp, args.filename).cmdloop()

if __name__ == "__main__":
    PYP = pyp.PyPass()
    PYPC = PyPassCli(PYP)
