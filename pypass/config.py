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

import os, ConfigParser, logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.addHandler(logging.NullHandler())

class PyPassConfig():

    def __init__(self):
        self.app_config_file = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
               'datas',
               'pypass.ini'
            )
         )

        self.config_dir = os.path.join(os.path.expanduser('~'), '.pypass')
        self.config_file = os.path.join(self.config_dir, 'pypass.ini')

        logger.debug('Application configuration file: %s' % self.app_config_file)
        logger.debug('Configuration file:             %s' % self.config_file)

        #Check if configuration directory exists, create it otherwise
        if not os.path.exists(self.config_dir):
            try:
                os.mkdir(self.config_dir)
                print 'PyPass configuration directory has been created in %s' % self.config_dir
            except MkdirError:
                sys.exit('Unable to create PyPass configuration directory under %s' % self.config_dir)

        config = ConfigParser.ConfigParser()
        config.read([self.app_config_file, self.config_file])

        #Rewrite local config to take care of new app changes
        logger.info('Update user config file')
        with open(self.config_file, 'wb') as configfile:
            config.write(configfile)

    def load(self):
        pass