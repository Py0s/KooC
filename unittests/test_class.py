#!/usr/bin/env python3

import unittest
import Knodes
from KoocGrammar import KoocG
from cnorm.passes import to_c

class Unittest_Class(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def setUp(self):
    	self.kooc_g = KoocG()

    def test_ClassIdentifierMangling(self):
        identifier = "MyClass"
        test = Knodes.Class(identifier)
        test.mangle()
        self.assertEqual(test.identifier, "K" + str(len(identifier)) + identifier)

    def test_ClasseEmpty(self):
        ast = self.kooc_g.parse("""
            @class Kyouma
            {}
            """)
        print(ast)
        self.assertEqual(ast.to_c(), (self.kooc_g.parse("""
            struct ~~~Kyouma~~~
            {}Kyouma;
            """)).to_c())

if __name__ == "__main__":
    unittest.main()