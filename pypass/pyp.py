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
import sys
import gnupg
import getpass
import json
import random

import logging
LOG = logging.getLogger(__name__)
if not LOG.handlers:
    LOG.addHandler(logging.NullHandler())

from . import __pypassconf__ as config
import pypobj

class PyPass(object):

    def __init__(self):
        try:
            self.random_number_generator = random.SystemRandom()
        except NotImplementedError:
            self.random_number_generator = random.Random()

        self._gnupgdir = os.path.join(os.path.expanduser('~'), '.gnupg')
        self._gpg = gnupg.GPG(gnupghome=self._gnupgdir, use_agent=True)
        self.data = None

    def load_data(self, passphrase=None, filename=None):
        """
        Decrypt and load datas into an internal object.

        See :func:`decrypt` for arguments details.
        """
        self.data = self.decrypt(passphrase=passphrase, filename=filename)

    def decrypt(self, passphrase=None, filename=None):
        """
        Decrypt a GPG encrypted file.

        If no passphrase is specified, we rely on GPG Agent to either grant the
        access to decrypt the file or ask your passphrase.

        If no filename is specified, we'll take the default one from
        configuration (~/.pypass/default.asc)
        """
        if filename is None:
            filename = config.file
        if os.path.exists(filename):
            LOG.debug(_("Opening file %s") % filename)
            stream = open(filename, 'rb')
            #have to select key before that
            decrypted_data = self._gpg.decrypt_file(
                                                   stream,
                                                   passphrase=passphrase)
            stream.close()
            if decrypted_data.ok:
                return decrypted_data.data
            else:
                LOG.warning(_("Could not decrypt file %s") % filename)
                #TODO: raise exception and cope with it
                #raise Exception("Could not decrypt file %s" % filename)
        else:
            LOG.warning(_('File %s does not exists.' % filename))
            return "{}"

    def crypt(self, recipients=None, filename=None, force=False):
        """
        Crypt file from current datas.

        You should specify one or more recipients:

        >>> crypt('ABCEDF')

        or

        >>> crypt(['ABCDEF', 'FEDCBA'])

        If no recipient is specified, we'll take the default from
        configuration.

        If no filename is specified, we'll take the default one from
        configuration (~/.pypass/default.asc)
        """
        if recipients is None:
            recipients = config.recipients
        if filename is None:
            filename = config.file
        if "override_file" in dir(config) and config.override_file:
            force = True
        print config.recipients, filename, self.data
        if config.recipients is None or config.recipients == "":
            return "key_not_found"
        if os.path.exists(filename):
            if not force:
                return "file_exists"
        edata = self._gpg.encrypt(
                                    self.data,
                                    recipients,
                                    output=filename)
        return edata.ok

    def add_password(self, database, model, itera, password):
        """ Add the given hashdict to the given database at the given
        level"""
        if itera is None or len(model[itera].path) ==  1 and \
            model[itera][2] != "folder":
            database.passwords.append(password)
        else:
            if len(model[itera].path) == 1:
                cnt = 0
                for directory in database.directories:
                    print directory.name, model[itera][0]
                    if directory.name == model[itera][0]:
                        database.directories[cnt].passwords.append(password)
                        return database
                    cnt = cnt + 1
            else:
                print "Trying to add a password into a folder"
                print model, itera, len(model[itera].path), \
                    model[itera].path, model[itera][2]
                print "Needs more logic than there currently is"
            #database.directories[level].append(passdict)
        return database

    def add_folder(self, database, model, itera, folder):
        """ Add the given folder to the given database at the given
        level"""
        if itera is None or len(model[itera].path) ==  1 and \
            model[itera][2] != "folder":
            database.directories.append(folder)
        else:
            if len(model[itera].path) == 1:
                cnt = 0
                for directory in database.directories:
                    print directory.name, model[itera][0]
                    if directory.name == model[itera][0]:
                        database.directories[cnt].directories.append(folder)
                        return database
                    cnt = cnt + 1
            else:
                print model, itera, len(model[itera].path), \
                    model[itera].path, model[itera][2]
                print "Needs more logic than there currently is"
            #database.directories[level].append(passdict)
        return database

    def data_from_json(self, data):
        """
        Set data from JSON
        """
        self.data = data.dump()
    
    def json_to_tree(self):
        """
        Transform the json into a tree from pypobj
        """
        return pypobj.json_to_tree(self.data_as_json())
        

    def data_as_json(self):
        """
        Get datas as JSON
        """
        return json.loads(self.data)

    def list_recipients(self):
        """
        List knows keys
        """
        return self._gpg.list_keys(True)

    def generate_error(self, errortext, error=None):
        """
        Function called when a error occurs.
        The error will be logged and program will exit.
        """
        LOG.error(errortext)
        LOG.error(error)
        sys.exit(1)

    def generate_password(self, password_length=None, character_set_ndx=None):
        """
        Random password generation. The above code was originally taken from
        gnome-password-generator.

        >>> p = PyPass()
        >>> p.generate_password()
        YViwf7h9vnp9

        If no password_length or character set is specified, we'll take those
        from the current configuration.
        """
        if password_length is None:
            password_length = config.passwords['length']
        if character_set_ndx is None:
            character_set_ndx = config.passwords['base']

        character_set = config.getCharacters(character_set_ndx)

        password = ""
        for current_character in range(password_length):
            random_number = self.random_number_generator.randint(0,
                                                    len(character_set) - 1)
            password += character_set[random_number]

        return password
    
    def is_default_in_keyring(self):
        """
        Check is the key set as default in the configuration file is installed
        on the computer
        """
        for key in self.list_recipients():
            if key["keyid"].endswith(config.recipients):
                return True
        return False
    
    def set_recipient(self, recipient):
        """
        Set the given recipient into the configuration
        """
        config.recipients = recipient
        #TODO: save the configuration

# for dev/testing purposes
if __name__ == "__main__":
    PPASS = PyPass()
    #print PPASS.list_recipients()
    #recipients = ['8BA59F94']
    #passphrase = getpass.getpass("Enter your GPG password:")
    #PPASS.load_data(passphrase)
    #PPASS.crypt(recipients)
    #PPASS.decrypt(passphrase = passphrase)
    print config.file
    config.file = '/a/file/whose/parent/path/does/not/exists'
    print config.file
