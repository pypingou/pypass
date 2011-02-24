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

from . import __pypassconf__ as config


class PyPass(object):

    def __init__(self):
        try:
            self.random_number_generator = random.SystemRandom()
        except NotImplementedError:
            self.random_number_generator = random.Random()

        self._gnupgdir = os.path.join(os.path.expanduser('~'), '.gnupg')
        self._gpg = gnupg.GPG(gnupghome=self._gnupgdir, use_agent=True)
        self.data = None

    def load_data(self, password=None, filename=None):
        """
        Decrypt and loads data into an internal object
        """
        self.data = self.decrypt(passphrase=password, filename=filename)

    def decrypt(self, passphrase=None, filename=None):
        """
        Decrypt file. If no file is specified, get its path from configuration
        """
        if filename is None:
            filename = config.file
        if os.path.exists(filename):
            print "opening file", filename
            stream = open(filename, 'rb')
            #have to select key before that
            decrypted_data = self._gpg.decrypt_file(
                                                   stream,
                                                   passphrase=passphrase)
            stream.close()
            if decrypted_data.ok:
                return decrypted_data.data
            else:
                print _("Could not decrypt file %s") % filename
                #TODO: raise exception and cope with it
                #raise Exception("Could not decrypt file %s" % filename)
        else:
            return "{}"

    def crypt(self, recipients=None, output=None):
        """
        Crypt file from current datas.

        If recipients are not set when calling the function, program will take
        the ones from configuration.
        """
        #have to select recipient before that
        if recipients is None:
            recipients = config.recipients
        if output is None:
            output = config.file
        edata = str(self._gpg.encrypt(
                                     self.data,
                                     recipients,
                                     output=output))
        return edata

    def add_password(self, database, level, passdict):
        """ Add the given hashdict to the given database at the given
        level"""
        if level in database.keys():
            database[level].append(passdict)
        else:
            database[level] = [passdict]
        return database

    def data_from_json(self, data):
        """
        Set data from JSON
        """
        self.data = json.dumps(data, indent=4)

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
        Function called when a error needs to be raised
        The error will be displayed in stdout
        """
        print errortext
        print error
        sys.exit(1)

    def generate_password(self, password_length=None, character_set_ndx=None):
        """
        Random password generation. The above code was originally taken from
        gnome-password-generator
        """
        if password_length is None:
            password_length = config.passwords['length']
        if character_set_ndx is None:
            character_set_ndx = config.passwords['base']

        character_set = config._character_sets[character_set_ndx].characters

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
