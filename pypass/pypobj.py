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

class PypDirectory(object):
    """ Represents a directory in pypass, used to classify the passwords """
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.content = []

class PypPasword(object):
    """ Represents a password in pypass"""
    
    def __init__(self, name, password, *args, **kw):
        self.name = name
        self.password = password
        print args, kw
