#!/usr/bin/env python3

import unittest
from .. import Knodes

class Unittest_Class(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def test_ClassIdentifierMangling(self):
        identifier = "MyClass"
        test = Knodes.Class(identifier)
        test.mangle()
        self.assertEqual(test.identifier, "K" + str(len(identifier)) + identifier)

if __name__ == "__main__":
    unittest.main()