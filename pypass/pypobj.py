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


def json_to_tree(jsontxt):
    """ From a given json structure transforms it to a tree """
    data = PypFolder("rootdir")
    if jsontxt is None:
        return data
    for key in jsontxt.keys():
        data = load_pypdir(jsontxt[key], key)
    return data


def load_pypdir(jsondir, name):
    """ convert an element of pypdir to tree """
    desc = None
    if "description" in jsondir.keys():
        desc = jsondir["description"]
    pypdir = PypFolder(name, desc)
    for password in jsondir["accounts"]:
        pypdir.accounts.append(load_password(password))
    for password in jsondir["folders"]:
        for key in password.keys():
            pypdir.folders.append(load_pypdir(
                                    password[key], key))
    return pypdir


def load_password(json_account):
    """ from an account entry in the json return a PypAccount object """
    pyppass = v(json_account["name"], json_account["password"])
    return pyppass


def create_set():
    """ Creates a fake PypFolder for development """
    root = PypFolder("rootfolder", "firstLevel")
    account = PypAccount("p1", "mdp1")
    root.accounts.append(account)
    account = PypAccount("p2", "mdp2")
    root.accounts.append(account)

    folder1 = PypFolder("secfolder", "secLevel")
    root.folders.append(folder1)
    account = PypAccount("p3", "mdp3")
    folder1.accounts.append(account)

    folder2 = PypFolder("thirdfolder", "thirdLevel")
    account = PypAccount("p4", "mdp4")
    folder2.accounts.append(account)
    folder1.folders.append(folder2)

    return root


def iterate_over_tree(obj, out, ite=0):
    """ Iterate over the items in a PypFolder """
    out = '%s "%s": { ' % (out, obj.name)
    if obj.description is not None and obj.description != "":
        out = '%s "description": "%s",' % (out, obj.description)
    ite = ite + 1
    cnt = 0
    out = '%s "accounts": [' % out
    for item in obj.accounts:
        cnt = cnt + 1
        out = '%s { "name": "%s", "password": "%s"}' % (out,
                item.name, item.password)
        if cnt != len(obj.accounts):
            out = "%s ," % out
    out = '%s ], ' % out
    out = '%s "folders": [{' % out
    cnt = 0
    for item in obj.folders:
        cnt = cnt + 1
        ite = ite + 1
        out = iterate_over_tree(item, out, ite)
        if cnt != len(obj.folders):
            out = "%s ," % out
    out = '%s }] }' % out
    return out


class PypFolder(object):
    """ Represents a folder in pypass, used to classify the accounts """

    def __init__(self, name="", description=None):
        self.name = name
        self.description = description
        self.accounts = []
        self.folders = []

    def dump(self):
        """ Dump the object to stdout """
        out = "{"
        out = iterate_over_tree(self, out)
        out = out + "}"
        return out


class PypAccount(object):
    """ Represents a password in pypass"""

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.extras = {}

#if __name__ == "__main__":
    #tree = create_set()
    #tree.dump()

    #import json
    #f = open("../testjson")
    #data = json.load(f)
    #f.close()
    #tree = json_to_tree(data)
    #tree.dump()
