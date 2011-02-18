#!/usr/bin/python
#-*- coding: utf-8 -*-

import pypass
from optparse import OptionParser

def getArgument():
    ''' Handle the parameters'''
    parser = OptionParser(version="%prog 0.0.1")
    parser.add_option("-f", "--file", dest="filename",
                help="The password database file")
    parser.add_option("--cli", dest="cli", default = False, action = "store_true",
                help="Start the cli interface instead of the gtk")

    
    return parser.parse_args()


if __name__ == "__main__":
    (options, args) = getArgument()
    if options.cli:
        pass
    else:
        options.filename = "../test.json"
        pypass.PyPass(options)

