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

import pypass
from pypass import pyp
from pypass import __version__, __application__, __description__
from pypass.gtk import gui


import logging
LOG = logging.getLogger(__name__)
if not LOG.handlers:
    try:
        LOG.addHandler(logging.NullHandler())
    except AttributeError:
        LOG.addHandler(pypass.PypNullHandler())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__description__,
                                     version="%(name)s GTK %(version)s" %
                          {'name': __application__, 'version': __version__})

    group = parser.add_argument_group(_('Common options'))
    group.add_argument('-f',
                       '--file',
                       dest='filename',
                       help=_('The password database file, this override '\
                              'the default value contained in the '\
                              'configuration file'))
    group.add_argument('-V',
                       '--verbose',
                       dest='verbose',
                       help=_('Be a bit more verbose.'),
                       action='store_true',
                       default=False)
    group.add_argument('-D',
                       '--debug',
                       dest='debug',
                       help=_('Activate debug mode (show executes commands, '\
                              'etc.).'),
                       action='store_true',
                       default=False)

    args = parser.parse_args()

    pyp = pyp.PyPass()
    try:
        gui.PyPassGui(pyp, args)
    except KeyboardInterrupt:
        LOG.warning(_("Exit on user request"))
