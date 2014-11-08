#!/usr/bin/env python3

import unittest
import __init__
import KoocGrammar
from KoocGrammar import KoocG
from KoocGrammar import Module
from cnorm.passes import to_c
import KoocFile

class UnittestNewtest(unittest.TestCase):

    def setUp(self):
        self.cparse = KoocG()

    def tearDown(self):
        self.cparse = None
        KoocFile.debugCleanAll()

    def test_module_simple_overload(self):
        print("THE FIRST TEST")
        res = str(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                float tuturu;
            }
            """).to_c())
        self.assertEqual(res,
                         "extern int M6Mayuri__i6tuturu;\nextern float M6Mayuri__f6tuturu;\n")

    def test_module_simple_overload_invalid(self):
        print("THE SECOND TEST")
        with self.assertRaises(RuntimeError) as cm:
            print(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                int tuturu;
            }
            """).to_c())
    def test_module_const_overload_invalid(self):
        print("THE THIRD TEST")
        with self.assertRaises(RuntimeError) as cm:
            print(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                const int tuturu;
            }
            """).to_c())
    def test_module_static_overload_invalid(self):
        with self.assertRaises(RuntimeError) as cm:
            print(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                static int tuturu;
            }
            """).to_c())

if __name__ == "__main__":
    unittest.main()
