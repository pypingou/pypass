#!/usr/bin/python

"""
Unit-tests for pypass
"""

import unittest
import sys
sys.path.insert(0, '..')

from pypass.pypobj import (json_to_tree, load_pypdir, load_account,
    create_set, iterate_over_tree)


class PyObjTestCase(unittest.TestCase):

    def test_create_set(self):
        """ Test the generation of a tree. """
        tree = create_set()
        self.assertEqual(tree.name, 'rootfolder')
        self.assertEqual(tree.folders[0].name, 'secfolder')
        self.assertEqual(tree.folders[0].folders[0].name, 'thirdfolder')

    def test_tree_to_json(self):
        """ Test the conversion of a tree to a json string. """
        tree = create_set()
        expected = '{"rootfolder": {  "description": "firstLevel", '\
        '"accounts": [ { "name": "p1", "password": "mdp1"} , '\
        '{ "name": "p2", "password": "mdp2"} ],  "folders": '\
        '[{"secfolder": {  "description": "secLevel", "accounts": '\
        '[ { "name": "p3", "password": "mdp3"} ],  "folders": '\
        '[{"thirdfolder": {  "description": "thirdLevel", "accounts": '\
        '[ { "name": "p4", "password": "mdp4"} ],  "folders": '\
        '[{ }] } }] } }] }}'
        self.assertEqual(tree.dump(), expected)

    def test_iterate_over_tree(self):
        """ Test the iteration over a tree. """
        tree = create_set()
        expected = '"thirdfolder": {  "description": "thirdLevel", '\
        '"accounts": [ { "name": "p4", "password": "mdp4"} ],  '\
        '"folders": [{ }] }'
        output = iterate_over_tree(tree.folders[0].folders[0], '')
        self.assertEqual(output, expected)

    def test_load_account(self):
        """ Test the load_account function. """
        tree = create_set()
        name = 'test_name'
        passw = 'test_password'
        url = 'http://example.org'
        desc = 'This is a test account'
        account = {'name': name,
                    'password': passw,
                    'url': url,
                    'description': desc
                    }
        output = load_account(account)
        self.assertEqual(output.name, name)
        self.assertEqual(output.extras['description'], desc)
        self.assertEqual(output.extras['url'], url)
        self.assertEqual(output.password, passw)

    def test_load_pydir(self):
        """ Test the load_pydir function. """
        json = {'description': 'This is a test folder',
                'accounts': [{'name': 'level2', 'password': 'mdplvl2'}],
                'folders': [{ }]
                }
        output = load_pypdir(json, 'test folder')
        self.assertEqual(output.name, 'test folder')
        self.assertEqual(output.description, 'This is a test folder')
        self.assertEqual(output.accounts[0].name, 'level2')
        self.assertEqual(output.accounts[0].password, 'mdplvl2')


if __name__ == '__main__':
    unittest.main()
