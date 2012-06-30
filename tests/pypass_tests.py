#!/usr/bin/python

"""
Unit-tests for pypass
"""

import unittest
import sys
sys.path.insert(0, '..')

from pypass.pyp import PyPass


class PyPassTestCase(unittest.TestCase):

    def test_load_data(self):
        pyp = PyPass()
        pyp.load_data('test')
        self.assertEqual(output, )


if __name__ == '__main__':
    unittest.main()
