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
import gnupg
import getpass
import json
import random

class PyPass():

    def __init__( self):
        self.character_sets = (
            CharacterSet("All printable (excluding space)", "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"),
            CharacterSet("Alpha-numeric (a-z, A-Z, 0-9)", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Alpha lower-case (a-z)", "abcdefghijklmnopqrstuvwxyz"),
            CharacterSet("Hexadecimal (0-9, A-F)", "0123456789ABCDEF"),
            CharacterSet("Decimal (0-9)", "0123456789"),
            CharacterSet("Base 64 (a-z, A-Z, 0-9, '+', '/')", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/")
        )

        try:
            self.random_number_generator = random.SystemRandom()
        except NotImplementedError:
            self.random_number_generator = random.Random()

        #File should be in ~/.pypass/
        #TODO: load configuration file
        self.hd = os.path.join(os.path.expanduser('~'), '.gnupg')
        #print self.hd
        self.gpg = gnupg.GPG(gnupghome=self.hd, use_agent=True)
        self.plain_file = 'test.json'
        self.filename = 'test.json.asc'

        self.data = self.decrypt()

    def decrypt(self):
        #TODO: we should work only from a stream, not from a file
        stream = open(self.filename, 'rb')
        #have to select key before that
        passphrase = getpass.getpass("Enter your GPG password:") 
        decrypted_data = self.gpg.decrypt_file(stream, passphrase=passphrase)
        return decrypted_data.data

    def crypt(self, recipients):
        #TODO: we should work only from a stream, not from a file
        stream = open(self.plain_file, 'rb')
        #have to select recipient before that
        edata = str(self.gpg.encrypt_file(stream, recipients, output=self.filename))

    def read_file(self):
        """Read the given json file and return the content """
        try:
            data = self.fio.readJson()
        except IOError, er:
            self.generate_error(
                "Something went wrong when trying to load the database:",
                er)
            return
        return data

    def add_password(self, database, level, passdict):
        """ Add the given hashdict to the given database at the given
        level"""
        if level in database.keys():
            database[level].append(passdict)
        else:
            database[level] = [passdict]
        return database

    def data_as_json(self):
        return json.loads(self.data)

    def generate_error(self, errortext, er = None):
        """ 
        Function called when a error needs to be raised
        The error will be displayed in stdout
        """
        print  errortext
        print er
        sys.exit(1)

    def generate_password(self, password_length = None, character_set_ndx = None):
        """
        Random password generation. The above code was originally taken from
        gnome-password-generator
        """
        if password_length is None:
            password_length = 12
        if character_set_ndx is None:
            character_set_ndx = 1

        character_set = self.character_sets[character_set_ndx].characters

        password = ""
        for current_character in range(password_length):
            random_number = self.random_number_generator.randint(0, len(character_set)-1)
            password += character_set[random_number]

        return password

# for dev/testing purposes
if __name__ == "__main__":
    p = PyPass()
    recipients = ['8BA59F94']
    p.crypt(recipients)
    p.decrypt()

class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters
