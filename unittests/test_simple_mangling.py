#!/usr/bin/env python3

import unittest
import mangler.simple_mangling as sm

class UnittestSimpleMangling(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def test_ident_mangling(self):
        ident = 'MyName'
        self.assertEqual(sm.id_m(ident), str(len(ident)) + ident)

    def test_type_mangling(self):
        res = sm.type_m('char')
        self.assertEqual(res, 'c')
        res = sm.type_m('signed char')
        self.assertEqual(res, 'Sc')
        res = sm.type_m('int')
        self.assertEqual(res, 'i')
        res = sm.type_m('int', sign = sm.S['UNSIGNED'])
        self.assertEqual(res, 'Ui')

        self.assertRaises(IndexError, sm.type_m, 'unknown')

    def test_qual_mangling(self):
        res = sm.qual_m('const')
        self.assertEqual(res, 'C_')
        self.assertRaises(IndexError, sm.qual_m, '')
