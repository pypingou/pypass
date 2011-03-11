#!/usr/bin/python

from distutils.core import setup
import os, sys
from pypass import __version__, __author__

name = 'PyPass'

locales = []
if os.path.exists('pypass/locale'):
    for lang in os.listdir('pypass/locale'):
        locales.append(os.path.join(lang, 'LC_MESSAGES'))

if sys.platform == 'win32':
    # Something might come here one day.
    pass
else:
    setup(
        name = name,
        version = __version__,
        packages = ['pypass', 
                    'pypass.gtk',
                    'pypass.gtk.ui',
                    ],
        package_data = {'pypass' : ['data/pypass.ini', 
                                'gtk/ui/*'] },
        scripts = ["pypass.py", "pypass-gtk.py"],
        license = 'GNU GPLv3 or any later version',
        description = 'Manage your passwords easily with PyPass',
        long_description = 'PyPass helps you to manage all your ' \
        'accounts in an easy and secure with GPG.',
        platforms = ['Linux'],
        author = __author__,
        author_email = 'admin@pypass.org',
        url = 'http://pypass.org',
        data_files = [("/usr/share/applications/",["PyPass.desktop"]), 
                      ('/usr/share/icons/PyPass.png',["pypass/data/logo.png"]),
                      #TODO: fix this when run from terminal (and not spec)
                    ]# + [(os.path.join(LOCALE_DIR, locale),
                       #     [os.path.join('pypass', 'locale', locale,
                       #      'pypass.mo')])
                       #     for locale in locales]
        )
