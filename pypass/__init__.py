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

"""
define some global variables
"""

__version__ = '0.0.1'
__date__ = '2011/02/21'
__author__ = ['Pierre-Yves `pingou` Chibon',
              'Johan `trashy` Cwiklinski']
__credits__ = ['Pierre-Yves `pingou` Chibon',
               'Johan `trashy` Cwiklinski',
               'Haïkel Guémar', 'Alexandrine Cwiklinski']
__license__ = 'GNU GPLv3 or any later version'
__copyright__ = 'Copyright (c) 2011 Pierre-Yves Chibon \n' \
                'Copyright (c) 2011 Johan Cwiklinski'
__url__ = 'http://pypass.org'
__status__ = "Prototype"
__license_text__ = """
PyPass is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

PyPass is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pypass; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
__description__ = 'Easily manage your passwords using Gnu Privacy Guard'
__mail__ = 'pypass@ulysses.fr'

import os
import sys
import errno
import gettext
import logging
#FIXME: should be import pypass.config, but does not work
import config

#logging stuff
LOG_FILENAME = os.path.join(os.path.expanduser('~'), '.pypass', 'pypass.log')
#Check if configuration directory exists, create it otherwise
if not os.path.exists(os.path.dirname(LOG_FILENAME)):
    try:
        os.mkdir(os.path.dirname(LOG_FILENAME))
        print ('PyPass configuration directory has been created in %s'
               % os.path.dirname(LOG_FILENAME))
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            sys.exit('Unable to create PyPass configuration directory under %s'
                     % os.path.dirname(LOG_FILENAME))

#set up logging to file - see previous section for more details
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
#define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
#set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s%(message)s')
#tell the handler to use this format
console.setFormatter(formatter)
#add the handler to the root logger
logging.getLogger('').addHandler(console)

__locale_dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'locale')

__application__ = 'pypass'
gettext.install(__application__, __locale_dir__)
