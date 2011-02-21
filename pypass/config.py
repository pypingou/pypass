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

import os
import ConfigParser
import logging
from . import *
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
        self._character_sets = (
            CharacterSet("All printable (excluding space)", "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"),
            CharacterSet("Alpha-numeric (a-z, A-Z, 0-9)", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Alpha lower-case (a-z)", "abcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Hexadecimal (0-9, A-F)", "0123456789ABCDEF"),
            CharacterSet("Decimal (0-9)", "0123456789"),
            CharacterSet("Base 64 (a-z, A-Z, 0-9, '+', '/')", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/")
        )

        self._file = os.path.expanduser(self.config.get('global', 'file'))
        self._recipients = self.config.get('global', 'recipients')
        self._passwords = {
            'length': int(self.config.get('password generator', 'length')),
            'base': int(self.config.get('password generator', 'base'))
        }

        logger.debug("Configuration loaded:\n- file: %s\n- recipients: %s\n- password length: %i\n- password base: %i" % (self._file, self.recipients, self.passwords_length, self.passwords_base))

    @property
    def file(self):
        """
        Getter for _file
        """
        return self._file

    @file.setter
    def file(self, value):
        """
        Setter for _file
        """
        if not os.path.exists(os.path.dirname(value)):
            logger.warn('Trying to set a value for file with a missing parent. ' + value)
            #FIXME: return something?
        else:
            logger.debug('Setting file to: ' + value)
            self._file = value

    @property
    def recipients(self):
        """
        Getter for recipients
        """
        return self._recipients

    @recipients.setter
    def recipients(self, value):
        """
        Setter for recipient
        """
        self._recipient = value

    @property
    def passwords(self):
        """
        Getter for passwords
        """
        return self._passwords

    @passwords.setter
    def passwords(self, value):
        """
        Prevent passwords modification. Use passwords_length and
        passwords_base attributes instead.
        """
        logger.warning('Trying to set passwords')

    @property
    def passwords_length(self):
        """
        Getter for password lenght
        """
        return self._passwords['length']

    @passwords_length.setter
    def passwords_length(self, value):
        """
        Setter for passwords length
        """
        #TODO: check if value is an integer
        self._passwords['length'] = value

    @property
    def passwords_base(self):
        """
        Getter for password base
        """
        return self._passwords['base']

    @passwords_base.setter
    def passwords_base(self, value):
        """
        Setter for passwords base
        """
        #TODO: check if value is an integer
        self._passwords['base'] = value

    @property
    def character_sets(self):
        """
        Characters sets getter
        """
        return self._character_sets

    def character_sets(self,value):
        """
        Prevent characters_sets modification.
        """
        logger.warning('Trying to change characters_sets')

class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters