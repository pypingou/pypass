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
import gettext

from pypass import pyp
from pypass import __version__, __application__
from pypass import __description__, __locale_dir__

gettext.install(__application__, __locale_dir__)


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

        query_group = parser.add_argument_group(_('Query options'))
        exclusive_query_group = query_group.add_mutually_exclusive_group(required = True)
        exclusive_query_group.add_argument('-l',
                                 '--list',
                                 help=_('List folders'),
                                 action='store_true',
                                 default=False)
        exclusive_query_group.add_argument('-g',
                                 '--get',
                                 help=_('Retrieve an account by its ID'),
                                 action='store',
                                 nargs='+',
                                 default=False)

        #exclusive = parser.add_mutually_exclusive_group()
        modif_group = parser.add_argument_group(_('Edition options'))
        modif_group.add_argument('-s',
                                '--save',
                                help=_('Save configuration in your '\
                                       'preferences file (%s).' %
                                       self.pyp.config.config_file),
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

        #Query
        if args.list:
            self.pyp.load_data(filename=args.filename)
            if self.pyp.data is not None and self.pyp.data != "":
                print self.pyp.data

        #Edition
        if args.save:
            self.pyp.config.writeUserConfig()

if __name__ == "__main__":
    PYP = pyp.PyPass()
    PYPC = PyPassCli(PYP)
