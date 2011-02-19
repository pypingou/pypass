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

class PyPass():

    def __init__( self):
        #File should be in ~/.pypass/
        self.hd = os.path.join(os.path.expanduser('~'), '.gnupg')
        #print self.hd
        self.gpg = gnupg.GPG(gnupghome=self.hd, use_agent=True)
        self.plain_file = 'test.json'
        self.crypted_file = 'test.json.asc'

    def decrypt(self):
        stream = open(self.crypted_file, 'rb')
        #have to select key before that
        passphrase = getpass.getpass("Enter your GPG password:") 
        decrypted_data = self.gpg.decrypt_file(stream, passphrase=passphrase)
        print decrypted_data.data

    def crypt(self, recipients):
        stream = open(self.plain_file, 'rb')
        #have to select recipient before that
        edata = str(self.gpg.encrypt_file(stream, recipients, output=self.crypted_file))
        
        #f = open(self.crypted_file, 'w')
        #f.write(edata)

# for dev/testing purposes
if __name__ == "__main__":
    p = PyPass()
    recipients = ['8BA59F94']
    p.crypt(recipients)
    p.decrypt()
