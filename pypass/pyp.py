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
    try:
        LOG.addHandler(logging.NullHandler())
    except AttributeError:
        LOG.addHandler(self.PypNullHandler())

import config
import pypass
import pypobj
from pypobj import PypDirectory, PypPassword


def get_directory_path(model, itera, directories):
        """
        For a given position in the model, browse the model up
        and add level by level the row name.
        This way we can browse the json back to the correct
        PypDirectory for our purpose.
        Returns None if the itera is not defined
        Returns [] for first level selection which are not folder
        """
        if itera is None:
            return
        if model[itera][2] == "folder":
            directories.append(model[itera][0])
        while model[itera].parent is not None and model[itera].parent != "":
            row = model[itera].parent
            get_directory_path(row.model, row.iter, directories)
            return directories
        return directories


class PyPass(object):

    def __init__(self):
        self.config = config.PyPassConfig()
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
            filename = self.config.file
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
            recipients = self.config.recipients
        if filename is None:
            filename = self.config.file
        #TODO: remove this dirty hack and change the config as it should be
        if "override_file" in dir(self.config) and self.config.override_file:
            force = True
        print recipients, filename, self.data
        if recipients is None or recipients == "":
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
        """ 
        Add the given hashdict to the given database at the given
        level
        
        To add a folder in the n level we need to be at the n level, 
        same goes for a password.
        """
        directoriespath = get_directory_path(model, itera, [])
        print directoriespath
        if itera is None or len(model[itera].path) == 1 and \
            model[itera][2] != "folder":
            if password.name in [passw.name for passw in database.passwords]:
                return "duplicate_entry"
            database.passwords.append(password)
        else:
            directoriespath.reverse()
            root = database
            for fold in directoriespath:
                for directory in root.directories:
                    if directory.name == fold:
                        root = directory
            if password.name in [passw.name for passw in root.passwords]:
                return "duplicate_entry"
            root.passwords.append(password)
        return database

    def add_folder(self, database, model, itera, folder):
        """ 
        Add the given folder to the given database at the given
        level
        
        To add a folder in the n level we need to be at the n level, 
        same goes for a password.
        """
        directoriespath = get_directory_path(model, itera, [])
        print directoriespath
        if directoriespath is None or len(directoriespath) == 0:
            if folder.name in [direc.name for direc in database.directories]:
                return "duplicate_entry"
            database.directories.append(folder)
        else:
            directoriespath.reverse()
            root = database
            for fold in directoriespath:
                for directory in root.directories:
                    if directory.name == fold:
                        root = directory
            if folder.name in [direc.name for direc in root.directories]:
                return "duplicate_entry"
            root.directories.append(folder)
        return database

    def replace_item(self, database, model, itera, item):
        """
        Replace an item base on the given coordinates
        
        To replace a folder in the n level we would need to be at the n-1 
        level, from there we can access the directories and update the 
        folder. However a folder does not get replaced but updated, 
        otherwise the lower part of the tree would get lost.
        
        On the other side, to replace a password we need to be at the n
        level (at the level of the folder containning this password).
        """
        directoriespath = get_directory_path(model, itera, [])
        if directoriespath is None or len(directoriespath) == 0:
            if isinstance(item, PypPassword):
                cnt = 0
                for passw in database.passwords:
                    if passw.name == model[itera][0]:
                        database.passwords[cnt] = item
                    cnt = cnt + 1
            else:
                print "bug"
        else:
            directoriespath.reverse()
            if isinstance(item, PypPassword):
                root = database
                for fold in directoriespath:
                    for directory in root.directories:
                        if directory.name == fold:
                            root = directory
                cnt = 0
                for passw in root.passwords:
                    if passw.name == model[itera][0]:
                        root.passwords[cnt] = item
                    cnt = cnt + 1
            else:
                root = database
                for fold in directoriespath:
                    for directory in root.directories:
                        if directory.name == fold:
                            root = directory

                root.name = item.name
                root.description = item.description
        return database

    def remove_item(self, database, model, itera, item):
        """ 
        Remove the item from the database using model and itera to access
        the item in the tree.
        
        To remove an item in the level n we need to be at n-1, therefore
        we only browse the directory tree down to the n-1 item.
        From there we can access the passwords/directories to remove
        the undesired item
        """
        directoriespath = get_directory_path(model, itera, [])
        if directoriespath is None or len(directoriespath) == 0:
            if isinstance(item, PypDirectory):
                database.directories.remove(item)
            else:
                database.passwords.remove(item)
        else:
            directoriespath.reverse()
            root = database
            for fold in directoriespath[:-1]:
                for directory in root.directories:
                    if directory.name == fold:
                        root = directory
            if isinstance(item, PypDirectory):
                root.directories.remove(item)
            else:
                root.passwords.remove(item)
        return database

    def get_item(self, database, directoriespath, typeitem, key):
        """ 
        For given coordinates return the corresponding object
        """
        root = database
        if directoriespath is not None and len(directoriespath) != 0:
            directoriespath.reverse()
            for fold in directoriespath:
                for directory in root.directories:
                    if directory.name == fold:
                        root = directory
            if typeitem == "folder":
                if root.name == key:
                    return root
                else:
                    print "bug"
            else:
                for passw in root.passwords:
                    if passw.name == key:
                        return passw
        else:
            if typeitem == "folder":
                if database.name == key:
                    return root
                else:
                    print "bug"
            else:
                for passw in database.passwords:
                    if passw.name == key:
                        return passw
        return 
        

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
            password_length = self.config.passwords['length']
        if character_set_ndx is None:
            character_set_ndx = self.config.passwords['base']

        character_set = self.config.getCharacters(character_set_ndx)

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
            if key["keyid"].endswith(self.config.recipients):
                return True
        return False

    def set_recipient(self, recipient):
        """
        Set the given recipient into the configuration
        """
        self.config.recipients = recipient
        #TODO: save the configuration

class PypNullHandler(logging.Handler):
    def emit(self, record):
        pass

# for dev/testing purposes
if __name__ == "__main__":
    PPASS = PyPass()
    #print PPASS.list_recipients()
    #recipients = ['8BA59F94']
    #passphrase = getpass.getpass("Enter your GPG password:")
    #PPASS.load_data(passphrase)
    #PPASS.crypt(recipients)
    #PPASS.decrypt(passphrase = passphrase)
    PPASS.config.file
    PPASS.config.file = '/a/file/whose/parent/path/does/not/exists'
    print PPASS.config.file
