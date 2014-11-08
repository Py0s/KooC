#!/usr/bin/env python3

import unittest
import __init__
import KoocGrammar
from KoocGrammar import KoocG
from KoocGrammar import Module
from cnorm.passes import to_c

class UnittestNewtest(unittest.TestCase):

    def setUp(self):
        self.cparse = KoocG()

    def test_module_simple_overload(self):
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
        with self.assertRaises(RuntimeError) as cm:
            print(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                int tuturu;
            }
            """).to_c())

if __name__ == "__main__":
    unittest.main()
