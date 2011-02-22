""" Object module for pypass 
This module contains the objects from and to which the json is
generated/read.
"""
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

def json_to_tree(json):
    """ From a given json structure transforms it to a tree """
    for key in json.keys():
        data = load_pypdir(json[key], key)
    return data

def load_pypdir(jsondir, name):
    """ convert an element of pypdir to tree """
    pypdir = PypDirectory(name, jsondir["description"])
    for password in jsondir["passwords"]:
        pypdir.passwords.append(load_password(password))
    for password in jsondir["directories"]:
        for key in password.keys():
            pypdir.directories.append(load_pypdir(
                                    password[key], key))
    return pypdir

def load_password(jsonpass):
    pyppass = PypPassword(jsonpass["name"], jsonpass["password"])
    return pyppass

def create_set():
    """ Creates a fake PypDirectory for development """
    root = PypDirectory("rootdir", "firstLevel")
    passw = PypPassword("p1","mdp1")
    root.passwords.append(passw)
    passw = PypPassword("p2","mdp2")
    root.passwords.append(passw)

    dir1 = PypDirectory("secdir", "secLevel")
    root.directories.append(dir1)
    passw = PypPassword("p3","mdp3")
    dir1.passwords.append(passw)

    dir2 = PypDirectory("thirdDir", "thirdLevel")
    passw = PypPassword("p4","mdp4")
    dir2.passwords.append(passw)
    dir1.directories.append(dir2)

    return root

def iterate_over_tree(obj, out, it = 0):
    """ Iterate over the items in a PypDirectory """
    out = '%s "%s": { ' % (out, obj.name)
    if obj.description is not None and obj.description != "":
        out = '%s "description": "%s",' % (out, obj.description)
    it = it + 1
    cnt = 0
    out = '%s "passwords": [' % out
    for item in obj.passwords:
        cnt = cnt +1
        out = '%s { "name": "%s", "password": "%s"}'  % (out, 
                item.name, item.password)
        if cnt != len(obj.passwords):
            out = "%s ," % out
    out = '%s ], ' % out
    out = '%s "directories": [{' % out
    for item in obj.directories:
        it = it + 1
        out = iterate_over_tree(item, out, it)
    out = '%s }] }' % out
    return out

class PypDirectory(object):
    """ Represents a directory in pypass, used to classify the passwords """

    def __init__(self, name="", description=None):
        self._name = name
        self._description = description
        self._passwords = []
        self._directories = []

    @property
    def name(self):
        """ Getter for name """
        return self._name

    @name.setter
    def name(self, value):
        """ Setter for name """
        self._name = value

    @property
    def description(self):
        """ Getter for description """
        return self._description

    @description.setter
    def description(self, value):
        """ Setter for description """
        self._description = value

    @property
    def passwords(self):
        """ Getter for passwords """
        return self._passwords

    @passwords.setter
    def passwords(self, value):
        """ Setter for passwords """
        self._passwords = value

    @property
    def directories(self):
        """ Getter for directories """
        return self._directories

    @directories.setter
    def directories(self, value):
        """ Setter for directories """
        self._directories = value

    def dump(self):
        """ Dump the object to stdout """
        out = "{"
        out = iterate_over_tree(self, out)
        out = out + "}"
        print out


class PypPassword(object):
    """ Represents a password in pypass"""
    
    def __init__(self, name, password, *args, **kw):
        self._name = name
        self._password = password
        #print args, kw

    @property
    def name(self):
        """ Getter for name """
        return self._name

    @name.setter
    def name(self, value):
        """ Setter for name """
        self._name = value

    @property
    def password(self):
        """ Getter for password """
        return self._password

    @password.setter
    def password(self, value):
        """ Setter for password """
        self._password = value

if __name__ == "__main__":
    tree = create_set()
    tree.dump()
    
    import json
    f = open("../testjson")
    data = json.load(f)
    f.close()
    tree = json_to_tree(data)
    tree.dump()
