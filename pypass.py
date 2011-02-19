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

from pypass import pypass
from pypass.gtk import gui
from optparse import OptionParser

def getArgument():
    ''' Handle the parameters'''
    parser = OptionParser(version="%prog 0.0.1")
    parser.add_option("-f", "--file", dest="filename",
                help="The password database file")
    parser.add_option("--cli", dest="cli", default = False, action = "store_true",
                help="Start the cli interface instead of the gtk")

    return parser.parse_args()

if __name__ == "__main__":
    (options, args) = getArgument()
    if options.cli:
        pass
    else:
        pypass = pypass.PyPass()
        gui.PyPassGui(pypass)

