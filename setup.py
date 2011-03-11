#!/usr/bin/python

# test via:
# python setup.py install --root /tmp/pypass && tree /tmp/pypass/

from distutils.core import setup
import os, sys
from pypass import __version__, __author__, __url__, __license__
from pypass import __description__, __mail__

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
                    ],
        package_data = {'pypass' : ['data/pypass.ini', 
                                'gtk/ui/*'] },
        scripts = ["pypass.py", "pypass-gtk.py"],
        license = __license__,
        description = __description__,
        long_description = 'PyPass helps you to manage all your ' \
        'accounts in an easy and secure with GPG.',
        platforms = ['Linux'],
        author = __author__,
        author_email = __mail__,
        url = __url__,
        data_files = [("/usr/share/applications/",["PyPass.desktop"]), 
                      ('/usr/share/icons/',["pypass/data/PyPass.png"]),
                      #TODO: fix language stuff
                    ]# + [(os.path.join(LOCALE_DIR, locale),
                       #     [os.path.join('pypass', 'locale', locale,
                       #      'pypass.mo')])
                       #     for locale in locales]
        )
