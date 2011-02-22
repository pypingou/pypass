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

def iterate_over_tree(obj, out, it = 0):
    """ Iterate over the items in a PypDirectory """
    out = '%s "%s": [ ' % (out, obj.name)
    it = it + 1
    cnt = 0
    for item in obj.content:
        cnt = cnt + 1
        if isinstance(item, PypDirectory):
            out = "%s ]," % out
            out = iterate_over_tree(item, out, it)
        else:
            out = '%s { "name": "%s", "password": "%s"}'  % (out, 
                    item.name, item.password)
            if cnt != len(obj.content) and \
             not isinstance(obj.content[cnt], PypDirectory):
                out = "%s ," % out
    return out

class PypDirectory(object):
    """ Represents a directory in pypass, used to classify the passwords """

    def __init__(self, name="", description=None):
        self._name = name
        self._description = description
        self._content = []

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
    def content(self):
        """ Getter for content """
        return self._content

    @content.setter
    def content(self, value):
        """ Setter for content """
        self._content = value
    
    def create_set(self):
        """ Creates a fake PypDirectory for development """
        root = PypDirectory("rootdir", "firstLevel")
        passw = PypPasword("p1","mdp1")
        root.content.append(passw)
        passw = PypPasword("p2","mdp2")
        root.content.append(passw)

        dir1 = PypDirectory("secdir", "secLevel")
        root.content.append(dir1)
        passw = PypPasword("p3","mdp3")
        dir1.content.append(passw)

        dir2 = PypDirectory("thirdDir", "thirdLevel")
        passw = PypPasword("p4","mdp4")
        dir2.content.append(passw)
        dir1.content.append(dir2)

        self.content = root

    def dump(self):
        """ Dump the object to stdout """
        out = "{"
        out = iterate_over_tree(self.content, out)
        out = out + " ]"
        out = out + "}"
        print out


class PypPasword(object):
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
    pypd = PypDirectory()
    tree = pypd.create_set()
    pypd.dump()
