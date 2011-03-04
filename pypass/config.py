""" Config module for pypass """
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
import gettext
import logging
from pypass import pyp
LOG = logging.getLogger(__name__)
if not LOG.handlers:
    try:
        LOG.addHandler(logging.NullHandler())
    except AttributeError:
        LOG.addHandler(pyp.PypNullHandler())


class PyPassConfig(object):
    """ Configuration class of pypass """

    def __init__(self):
        self.app_config_file = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
               'data',
               'pypass.ini'
            )
         )

        self.config_dir = os.path.join(os.path.expanduser('~'), '.pypass')
        self.config_file = os.path.join(self.config_dir, 'pypass.ini')

        LOG.debug(_('Application configuration file: %s') %
                    self.app_config_file)
        LOG.debug(_('Configuration file:             %s') %
                    self.config_file)

        self.config = ConfigParser.ConfigParser()
        self.config.read([self.app_config_file, self.config_file])

        #we're done with initialization, we can load values now
        self.load()

    def load(self):
        """
        Load configuration
        """
        self._character_sets = (
            CharacterSet(_("All printable (excluding space)"), "!\"#$%&'()"\
                "*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"\
                "abcdefghijklmnopqrstuvwxyz{|}~"),
            CharacterSet(_("Alpha-numeric (a-z, A-Z, 0-9)"), "0123456789"\
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
            CharacterSet(_("Alpha lower-case (a-z)"), "abcdefghijklmno"\
                "pqrstuvwxyz"),
            CharacterSet(_("Hexadecimal (0-9, A-F)"), "0123456789ABCDEF"),
            CharacterSet(_("Decimal (0-9)"), "0123456789"),
            CharacterSet(_("Base 64 (a-z, A-Z, 0-9, '+', '/')"), "0123456789"\
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/")
        )

        self._file = os.path.expanduser(self.config.get('global', 'file'))
        self._recipients = self.config.get('global', 'recipients')
        self._passwords = {
            'length': int(self.config.get('password generator', 'length')),
            'base': int(self.config.get('password generator', 'base'))
        }

        LOG.debug(_("Configuration loaded:\n- file: %(file)s\n- recipients: "\
            "%(recipients)s\n- password length: %(passlength)i\n- "\
            "password base: %(passbase)i") % {
            'file': self._file,
            'recipients': self.recipients,
            'passlength': self.passwords_length,
            'passbase': self.passwords_base})

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
            LOG.warn(_('Trying to set a value for file with a missing ' \
                'parent. %s') % value)
            #FIXME: return something?
        else:
            LOG.debug(_('Setting file to: %s') % value)
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
        LOG.warning(_('Trying to set passwords'))

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

    def character_sets(self, value):
        """
        Prevent characters_sets modification.
        """
        LOG.warning(_('Trying to change characters_sets'))

    def getCharacters(self, index):
        """
        Return the selected character set. The function will first check if
        the given index is in the correct range, and defaults to 1 if not.

        For example:

        >>> getCharacterSet(3)

        Will return the hexadecimal character set, while:

        >>> getCharacterSet(10)
        >>> getCharacterSet(50)
        >>> getCharacterSet(-1)

        Will both return alphanumeric character.
        """
        length = len(self._character_sets)
        if not 0 <= index < length:
            LOG.warning(_('Trying to get index %(index)d for a %(items)d '\
                        'items list; switching index to %(default)d ') %
                        {'index': index, 'items': length, 'default': default})
            #characters set from index 0 is too large
            index = 1
        set = self._character_sets[index]
        LOG.debug(_('Retrieving character set %(index)d (%(name)s, '\
                    '`%(chars)s`)') %
                  {'index': index, 'name': set.description,
                   'chars': set.characters})
        return set.characters

    def writeUserConfig(self):
        #Rewrite local config to take care of new app changes
        LOG.info(_('Update user config file'))
        with open(self.config_file, 'wb') as configfile:
            self.config.write(configfile)


class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters
