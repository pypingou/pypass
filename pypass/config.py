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

class PyPassConfig(object):

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

        #Check if configuration directory exists, create it otherwise
        if not os.path.exists(self.config_dir):
            try:
                os.mkdir(self.config_dir)
                logger.info('PyPass configuration directory has been created in %s' % self.config_dir)
            except MkdirError:
                logger.exception('Unable to create PyPass configuration directory under %s' % self.config_dir)
                sys.exit('Unable to create PyPass configuration directory under %s' % self.config_dir)

        logger.debug('Application configuration file: %s' % self.app_config_file)
        logger.debug('Configuration file:             %s' % self.config_file)

        self.config = ConfigParser.ConfigParser()
        self.config.read([self.app_config_file, self.config_file])

        #Rewrite local config to take care of new app changes
        logger.info('Update user config file')
        with open(self.config_file, 'wb') as configfile:
            self.config.write(configfile)

        #we're done with initialization, we can load values now
        self.load()

    def load(self):
        """
        Loads configuration
        """
        self.character_sets = (
            CharacterSet("All printable (excluding space)", "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"),
            CharacterSet("Alpha-numeric (a-z, A-Z, 0-9)", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Alpha lower-case (a-z)", "abcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Hexadecimal (0-9, A-F)", "0123456789ABCDEF"),
            CharacterSet("Decimal (0-9)", "0123456789"),
            CharacterSet("Base 64 (a-z, A-Z, 0-9, '+', '/')", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/")
        )

        self._file = os.path.expanduser(self.config.get('global', 'file'))
        self.recipients = self.config.get('global', 'recipients')
        self.passwords = {
            'length': int(self.config.get('password generator', 'lenght')),
            'base': int(self.config.get('password generator', 'base'))
        }

        logger.debug("Configuration loaded:\n- file: %s\n- recipients: %s\n- password length: %i\n- password base: %i" % (self._file, self.recipients, self.passwords['length'], self.passwords['base']))

    @property
    def file(self):
        """
        Getter for _file
        """
        #FIXME: we do not pass here :/
        return self._file

    @file.setter
    def file(self, value):
        """
        Setter for _file
        """
        #FIXME: we do not pass here :/
        if os.path.exists(os.path.dirname(value)):
            logger.warn('Trying to set a value for file with a missing parent. ' + value)
            #FIXME: return something?
        else:
            self._file = value

class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters