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

#define some global variables


__version__   = '0.0.1'
__date__      = '2011/02/21'
__author__    = 'Pierre-Yves `pingou` Chibon' \
                'Johan `trashy` Cwiklinski'
__copyright__ = 'Copyright (c) 2011 Pierre-Yves Chibon - Copyright (c) 2011 Johan Cwiklinski'
__url__       = 'https://redmine.ulysses.fr/projects/pypass'
__status__    = "Prototype"

import os
import logging
import config

#logging stuff
LOG_FILENAME = os.path.join(os.path.expanduser('~'), '.pypass', 'pypass.log')
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
locale_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locale')
pypassconf = config.PyPassConfig()

#TODO: i18n
#import gettext
#application = 'pypass'
#gettext.install(application, locale_dir)
#credits = _('')
