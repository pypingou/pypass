#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2011 Johan Cwiklinski <johan AT x-tnd DOT be>
#
# This file is part of PyPass.
#
# PyPass is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyPass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyPass.  If not, see <http://www.gnu.org/licenses/>.

"""
PyPass: Easily manage your passwords using Gnu Privacy Guard

gettext management (update, create files, compile, ...)
"""

import argparse
import sys
import os
import glob
import subprocess
from pypass import __version__, __author__, __locale_dir__, __application__
from pypass import __mail__


class PyPassGetText:

    def __init__(self):
        self.locale_dir = __locale_dir__

    def update(self):
        global args
        if args.verbose:
            print 'Update all'
        self.updateFromSources()
        self.updateTranslations()
        if not args.sources and not args.translations:
            print 'Full update complete.'

    def updateFromSources(self):
        global args
        if args.verbose:
            print 'Updating main catalog from sources...'
        cmd = [
               'xgettext',
               '--copyright-holder',
               ', '.join(__author__),
               '--package-name',
               __application__,
               '--package-version',
               __version__,
               '--msgid-bugs-address',
               __mail__,
               '-k_',
               '-kN_',
               '-o',
               '%s.pot' % __application__
               ]
        #include python files
        cmd.extend(glob.glob(os.path.join(os.getcwd(), '*.py')))
        cmd.extend(glob.glob(os.path.join(os.getcwd(), 'pypass', '*.py')))
        cmd.extend(glob.glob(os.path.join(os.getcwd(), 'pypass', 'gtk',
                                          '*.py')))
        #include glade files
        cmd.extend(glob.glob(os.path.join(os.getcwd(), 'pypass', 'gtk',
                                          'ui', '*.glade')))
        if args.debug:
            print cmd
            print ' '.join(cmd)
        subprocess.call(cmd)
        if args.sources or args.verbose:
            print 'Main catalog has been updated from sources.'

    def updateTranslations(self):
        global args
        if args.verbose:
            print 'Updating po files from main catalog...'

        for trans in glob.glob(os.path.join(self.locale_dir,
                                            '*/LC_MESSAGES/*.po')):
            cmd = [
                   'msgmerge',
                   '-U',
                   trans,
                   '%s.pot' % __application__
                   ]
            if args.debug:
                print cmd
            subprocess.call(cmd)
        if args.translations or args.verbose:
            print 'All catalogs has been updated from main catalog.'

    def createLanguage(self, langs):
        global args
        if args.verbose:
            print 'About to create catalogs for languages:', ', '.join(langs)

        for lang in langs:
            lang_path = os.path.join(os.getcwd(), self.locale_dir, lang[:2],
                                     'LC_MESSAGES')
            lang_file = os.path.join(lang_path, '%s.po' % __application__)
            if args.verbose:
                print 'Creating catalog for language %s in %s' % (lang,
                                                                 lang_path)
            if os.path.exists(lang_path) and os.path.exists(lang_file):
                sys.exit('Path %s already exists. Are you sure you do not '\
                         'mean update?\nAborting.' % lang_path)
            else:
                if not os.path.exists(lang_path):
                    os.makedirs(lang_path)
                cmd = [
                       'msginit',
                       '--locale',
                       lang,
                       '-i',
                       '%s.pot' % __application__,
                       '-o',
                       lang_file
                       ]
                if args.debug:
                    print cmd
                subprocess.call(cmd)
                if args.verbose:
                    print 'New catalog for language %s has been '\
                    'created.' % lang
        print 'New catalogs has been created for languages: ', ', '.join(langs)

    def compile(self):
        global args
        if args.verbose:
            print 'Compiling PO files...'
        for trans in glob.glob(os.path.join('.', self.locale_dir,
                                            '*/LC_MESSAGES/*.po')):
            cmd = [
                   'msgfmt',
                   trans,
                   '-o',
                   trans.replace('.po', '.mo')
                   ]
            if args.debug:
                print cmd
            r = subprocess.call(cmd)
            if r == 0:
                print 'PO files has been compiled.'
            else:
                print 'An error occurs. Please see above output to know '\
                'more. You can try again using -V or -D options.'

    def localeDirPresent(self):
        """
        Checks if locale directory exists
        """
        return os.path.exists(self.locale_dir)

if __name__ == '__main__':
    rb = PyPassGetText()
    if not rb.localeDirPresent():
        sys.exit('Locale dir (%s) cannot be found. Please create it '\
                 'before proceed.' % rb.locale_dir)

    parser = argparse.ArgumentParser(description='PyPass - I18N',
                                     version=__version__)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u',
                       '--update',
                       help='Full i18n update',
                       action='store_true',
                       default=False)
    group.add_argument('-s',
                       '--sources',
                       help='Update main catalog from sources',
                       action='store_true',
                       default=False)
    group.add_argument('-t',
                       '--translations',
                       help='Update translations from main catalog',
                       action='store_true',
                       default=False)
    group.add_argument('-n',
                       '--new',
                       dest='langs',
                       help='Create new language',
                       action='store',
                       nargs="+")

    parser.add_argument('-c',
                        '--compile',
                        help='Compile po files',
                        action='store_true',
                        default=False)

    more_group = parser.add_argument_group('Debugging option')
    more_group.add_argument('-V',
                            '--verbose',
                            help='Be more verbose',
                            action='store_true',
                            default=False)
    more_group.add_argument('-D',
                            '--debug',
                            help='Run in "debug" mode (show commands, etc.)',
                            action='store_true',
                            default=False)

    args = parser.parse_args()

    if args.debug:
        print args

    if args.langs:
        rb.createLanguage(args.langs)
    elif args.translations:
        rb.updateTranslations()
    elif args.sources:
        rb.updateFromSources()
    elif args.update:
        rb.update()
    elif args.compile:
        rb.compile()
    else:
        print 'Please specify a parameter.'
        parser.print_help()
